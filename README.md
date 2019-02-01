# PiHole-Panel
![](https://raw.githubusercontent.com/daleosm/PiHole-Panel/master/mainwindow.png)


PiHole-Panel 1.8
- Now works with package manager
- Fixed handling of when Pi-hole host is down
- Fixed update notification

Upcoming features:
  - Ability to use multiple Pi-hole hosts
  - Live tracking of DNS requests

## Install

Install/Update:
```
sudo apt install python3-gi
```
```
cd ~/Downloads
sudo dpkg -i PiHole-Panel-1.8.deb
```

Uninstall:
```
sudo apt remove pihole-panel
```

Troubleshoot:
```
rm ~/.config/pihole_panel_configs.xml
```
