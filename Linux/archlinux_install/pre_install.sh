#!/bin/bash

set -e 

systemctl stop reflector.service
cp mirrorlist /etc/pacman.d/mirrorlist
