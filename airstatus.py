#!/usr/bin/env python3
from bleak import BleakScanner
from time import sleep
from binascii import hexlify
from json import dumps
from datetime import datetime
from os import makedirs, path, getenv
import asyncio
from typing import Dict, Any, Optional

# Configure update duration (update after n seconds)
UPDATE_DURATION = 1
MIN_RSSI = -60
AIRPODS_MANUFACTURER = 76
AIRPODS_DATA_LENGTH = 54
RECENT_BEACONS_MAX_T_NS = 10000000000  # 10 Seconds

recent_beacons: list[Dict[str, Any]] = []


def get_best_result(device: Any, adv_data: Any) -> Any:
    try:
        from time import time_ns
    except ImportError:
        from datetime import datetime

        def time_ns() -> int:
            now = datetime.now()
            return int(now.timestamp() * 1e9)

    current_beacon = {"time": time_ns(), "device": device, "adv_data": adv_data}
    recent_beacons.append(current_beacon)
    strongest_beacon = None
    i = 0
    while i < len(recent_beacons):
        if time_ns() - recent_beacons[i]["time"] > RECENT_BEACONS_MAX_T_NS:
            recent_beacons.pop(i)
            continue
        if (
            strongest_beacon is None
            or strongest_beacon["adv_data"].rssi < recent_beacons[i]["adv_data"].rssi
        ):
            strongest_beacon = recent_beacons[i]
        i += 1

    if (
        strongest_beacon is not None
        and strongest_beacon["device"].address == device.address
    ):
        strongest_beacon = current_beacon

    if strongest_beacon is None:
        raise ValueError("No valid beacon found")

    return strongest_beacon["adv_data"]


# Getting data with hex format
async def get_device() -> Optional[bytes]:
    # Scanning for devices
    discovered_devices_and_advertisement_data = await BleakScanner.discover(
        return_adv=True
    )
    for device, adv_data in discovered_devices_and_advertisement_data.values():
        # Checking for AirPods
        try:
            adv_data = get_best_result(device, adv_data)
        except ValueError:
            continue

        if (
            adv_data.rssi >= MIN_RSSI
            and AIRPODS_MANUFACTURER in adv_data.manufacturer_data
        ):
            data_hex = hexlify(
                bytearray(adv_data.manufacturer_data[AIRPODS_MANUFACTURER])
            )
            data_length = len(
                hexlify(bytearray(adv_data.manufacturer_data[AIRPODS_MANUFACTURER]))
            )
            if data_length == AIRPODS_DATA_LENGTH:
                return data_hex
    return None


# Same as get_device() but it's standalone method instead of async
def get_data_hex() -> Optional[bytes]:
    a = asyncio.run(get_device())
    return a


# Getting data from hex string and converting it to dict(json)
def get_data() -> Dict[str, Any]:
    raw = get_data_hex()

    # Return blank data if airpods not found
    if raw is None:
        return dict(status=0, model="AirPods not found")

    flip: bool = is_flipped(raw)

    # On 7th position we can get AirPods model, gen1, gen2, Pro or Max
    if chr(raw[7]) == "2":
        model = "AirPods1"
    elif chr(raw[7]) == "f":
        model = "AirPods2"
    elif chr(raw[7]) == "3":
        model = "AirPods3"
    elif chr(raw[7]) == "9":
        model = "AirPods4"
    elif chr(raw[7]) == "b":
        model = "AirPods4ANC"
    elif chr(raw[7]) == "e":
        model = "AirPodsPro"
    elif chr(raw[7]) == "4":
        model = "AirPodsPro2"
    elif chr(raw[7]) == "a":
        model = "AirPodsMax"
    else:
        model = "unknown"

    # Checking left AirPod for availability and storing charge in variable
    status_tmp = int("" + chr(raw[12 if flip else 13]), 16)
    left_status = (
        100 if status_tmp == 10 else (status_tmp * 10 + 5 if status_tmp <= 10 else -1)
    )

    # Checking right AirPod for availability and storing charge in variable
    status_tmp = int("" + chr(raw[13 if flip else 12]), 16)
    right_status = (
        100 if status_tmp == 10 else (status_tmp * 10 + 5 if status_tmp <= 10 else -1)
    )

    # Checking AirPods case for availability and storing charge in variable
    status_tmp = int("" + chr(raw[15]), 16)
    case_status = (
        100 if status_tmp == 10 else (status_tmp * 10 + 5 if status_tmp <= 10 else -1)
    )

    # On 14th position we can get charge status of AirPods
    charging_status = int("" + chr(raw[14]), 16)
    charging_left: bool = (charging_status & (0b00000010 if flip else 0b00000001)) != 0
    charging_right: bool = (charging_status & (0b00000001 if flip else 0b00000010)) != 0
    charging_case: bool = (charging_status & 0b00000100) != 0

    # Return result info in dict format
    return dict(
        status=1,
        charge=dict(left=left_status, right=right_status, case=case_status),
        charging_left=charging_left,
        charging_right=charging_right,
        charging_case=charging_case,
        model=model,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        raw=raw.decode("utf-8"),
    )


# Return if left and right is flipped in the data
def is_flipped(raw: bytes) -> bool:
    return (int("" + chr(raw[10]), 16) & 0x02) == 0


def run() -> None:
    output_dir = f"{getenv('HOME')}/.var/airstatus"
    output_file = f"{output_dir}/out.json"

    if not path.exists(output_dir):
        makedirs(output_dir)

    try:
        while True:
            data = get_data()

            if data["status"] == 1 and data["model"] != "unknown":
                json_data = dumps(data)
                with open(output_file, "w") as f:
                    f.write(json_data + "\n")

            sleep(UPDATE_DURATION)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()
