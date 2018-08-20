#!/bin/bash

SUDO=''
if (( $EUID != 0 )); then
    SUDO='sudo'
fi

cd /tmp
$SUDO wget https://github.com/daleosm/PiHole-Panel/archive/master.zip
$SUDO unzip