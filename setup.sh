#!/bin/bash

SUDO=''
if (( $EUID != 0 )); then
    SUDO='sudo'
fi

cd /tmp
$SUDO wget https://github.com/daleosm/PiHole-Panel/archive/master.zip
$SUDO unzip master.zip
$SUDO rm master.zip

cd PiHole-Panel-master/
$SUDO mv bin/pihole-panel /usr/bin
$SUDO mv pihole-panel /usr/lib
$SUDO mv pihole-panel.desktop /usr/share/applications
$SUDO rm -R /tmp/PiHole-Panel-master

echo "Done!"