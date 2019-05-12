# PiHole-Panel

![](https://raw.githubusercontent.com/daleosm/PiHole-Panel/master/main_window.png)
PiHole-Panel 2.0
- Changes to API now require 3 second update interval.

PiHole-Panel 1.9
- Now compatible with latest API
- Temporary fix for Gravity Last Updated

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
