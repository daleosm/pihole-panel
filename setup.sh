#!/bin/bash

cd /tmp
wget https://github.com/daleosm/PiHole-Panel/archive/master.zip
unzip master.zip
rm master.zip

# Keep things tidy
if [ -e ~/.config/gtk_assistant_configs.xml ]; then
    mv ~/.config/gtk_assistant_configs.xml ~/.config/pihole_panel_configs.xml
fi

cd PiHole-Panel-master/
mv -f bin/pihole-panel /usr/bin
rm -r -f /usr/lib/pihole-panel
mv -f pihole-panel /usr/lib
mv -f pihole-panel.desktop /usr/share/applications
rm -R /tmp/PiHole-Panel-master

echo "Done!"
