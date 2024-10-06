# **AirStatus for Linux**
#### Check your AirPods battery level on Linux

#### What is it?
This is a Python program, forked from [faglo/AirStatus](https://github.com/faglo/AirStatus) that reads your AirPods' battery levels and writes them into a JSON file.

### Installation
#### Clone the repository.

`git clone https://github.com/carmen-outsold/AirStatus.git`

#### Change directory.

`cd AirStatus`

#### Make the `install.sh` script executable.
`chmod +x install.sh`

#### Run the script.

`./install.sh`

### Systemd service

Start and enable the service on boot:
 ```
sudo systemctl enable --now airstatus
```

### Usage

The script will be automatically run by the service. Output will be stored in `out.json` located at `$HOME/.var/airstatus`.

#### Example output

```
{"status": 1, "charge": {"left": 95, "right": 95, "case": -1}, "charging_left": false, "charging_right": false, "charging_case": false, "model": "AirPodsPro", "date": "2021-12-22 11:09:05"}
```

#### Used materials
* Some code from [this repo](https://github.com/ohanedan/Airpods-Windows-Service)
