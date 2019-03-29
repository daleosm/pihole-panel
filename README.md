# PiHole-Panel
PiHole-Panel is a control panel and real-time statistics for the Pi-hole Adblocker. 

![](https://raw.githubusercontent.com/daleosm/PiHole-Panel/master/main_window.png)

PiHole-Panel 1.9
- Now compatible with latest API
- Created temporary fix for Gravity Last Updated

PiHole-Panel 1.8
- Now works with package manager
- Fixed handling of when Pi-hole host is down
- Fixed update notification

Upcoming features:
  - Ability to use multiple Pi-hole hosts
  - Live tracking of DNS requests

## Install/Update
```
sudo apt install python3-gi
```
```
cd ~/Downloads
sudo dpkg -i PiHole-Panel-latest.deb
```

## Uninstall
```
sudo apt remove pihole-panel
```

## Troubleshoot
```
rm ~/.config/pihole_panel_configs.xml
```
