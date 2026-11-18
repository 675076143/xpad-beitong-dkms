#!/bin/sh
# Read-only; no sudo, module loading, USB requests or device permission changes.
# Inspect USB output for serial numbers before sharing.
date -Is
uname -r
pacman -Q xpad-beitong-dkms
printf '\nDisk module:\n'
modinfo -F filename xpad
modinfo -F srcversion xpad
printf '\nLive module srcversion:\n'
cat /sys/module/xpad/srcversion
printf '\nNext modprobe selection (dry run):\n'
modprobe --show-depends xpad
printf '\nUSB identity and bindings:\n'
lsusb
lsusb -t
