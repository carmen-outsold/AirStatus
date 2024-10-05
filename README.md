# **AirStatus for Linux**
#### Check your AirPods battery level on Linux

#### What is it?
This is a Python script, forked from [faglo/AirStatus](https://github.com/faglo/AirStatus) that reads your airpods' battery levels and writes into a JSON file.

### Usage
Make sure you have python 3.12 and bleak 0.22.3 installed.

```
python3 main.py
```

Output will be stored in `out.json` located at `$HOME/.var/airstatus`.

#### Example output

```
{"status": 1, "charge": {"left": 95, "right": 95, "case": -1}, "charging_left": false, "charging_right": false, "charging_case": false, "model": "AirPodsPro", "date": "2021-12-22 11:09:05"}
```

### Installing as a service

Create the file `/etc/systemd/system/airstatus.service` (as root) containing:
```
[Unit]
Description=Airpods Battery Monitor

[Service]
ExecStart=/usr/bin/python3 /PATH/TO/AirStatus/main.py
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
```

Start the service:
```
sudo systemctl start airstatus
```

Enable service on boot:
 ```
sudo systemctl enable airstatus
```
#### Used materials
* Some code from [this repo](https://github.com/ohanedan/Airpods-Windows-Service)
