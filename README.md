# **AirStatus for Linux**
#### Check your AirPods' battery levels on Linux

### Installation
#### Clone the repository
```
git clone https://github.com/carmen-outsold/AirStatus.git
```

#### Change directory
```
cd AirStatus
```

#### Make the `install.sh` script executable
```
chmod +x install.sh
```

#### Run the script
```
./install.sh
```
### Systemd service

Start and enable the service on boot:
```
sudo systemctl enable --now airstatus.service
```

### Usage

The script will be automatically run by the service. Output will be stored in `out.json` located at `$HOME/.var/airstatus`.

There's also a WIP KDE Plasma Widget for [airstatus](https://github.com/carmen-outsold/airstatus-plasmoid).

#### Example output

```
{
   "status":1,
   "charge":{
      "left":95,
      "right":95,
      "case":-1
   },
   "charging_left":false,
   "charging_right":false,
   "charging_case":false,
   "model":"AirPodsPro",
   "date":"2021-12-22 11:09:05"
}
```

#### Credits
* Forked from [faglo/AirStatus](https://github.com/faglo/AirStatus).
* Some code from [ohanedan/Airpods-Windows-Service](https://github.com/ohanedan/Airpods-Windows-Service).
