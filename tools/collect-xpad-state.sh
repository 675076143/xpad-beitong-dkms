#!/bin/sh
# Read-only; never loads modules or changes USB state/permissions.
# Prints only Beitong USB IDs/interface bindings, never USB serials or other devices.
probe() {
    printf '\n%s:\n' "$1"
    shift
    "$@"
    status=$?
    if [ "$status" -ne 0 ]; then
        printf '[unavailable; exit=%s]\n' "$status"
    fi
    return 0
}
probe Timestamp date -Is
probe Kernel uname -r
probe Package pacman -Q xpad-beitong-dkms
probe Disk-module-path modinfo -F filename xpad
probe Disk-srcversion modinfo -F srcversion xpad
probe Live-srcversion cat /sys/module/xpad/srcversion
probe Beitong-USB python3 - <<'PYUSB'
from pathlib import Path
root = Path('/sys/bus/usb/devices')
if not root.is_dir():
    raise SystemExit('USB sysfs unavailable')
found = False
for device in sorted(root.iterdir()):
    if ':' in device.name:  # USB interfaces have no device-level idVendor.
        continue
    try:
        vendor = (device / 'idVendor').read_text().strip()
        if vendor not in ('20bc', '20dd'):
            continue
        product = (device / 'idProduct').read_text().strip()
        print(f'{device.name} {vendor}:{product}')
        found = True
        for interface in sorted(root.glob(device.name + ':*')):
            driver = interface / 'driver'
            print(' interface', interface.name, 'driver',
                  driver.resolve().name if driver.is_symlink() else 'unbound')
    except (OSError, ValueError) as error:
        print('[USB state changed or inaccessible:', type(error).__name__ + ']')
if not found:
    print('No readable Beitong USB device (20bc/20dd)')
PYUSB
