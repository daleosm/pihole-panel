#!/bin/bash

cd /tmp
wget https://github.com/daleosm/PiHole-Panel/archive/master.zip
unzip master.zip
rm master.zip

cd PiHole-Panel-master/
mv -f bin/pihole-panel /usr/bin
mv -f pihole-panel /usr/lib
mv -f pihole-panel.desktop /usr/share/applications
rm -R /tmp/PiHole-Panel-master

echo "Done!"
