# xpad-beitong-dkms

**Temporary** DKMS module for patched `xpad` with Beitong KP-series 2.4G gamepad fix. Will be deprecated once the patch is merged upstream (expected Linux 7.3 or later).

## Problem

Beitong (北通) KP-series gamepads (KP20A, KP40A, KP50B, etc.) disconnect every ~1s when using the 2.4G wireless receiver on Linux. The firmware detects the host OS and power-cycles the USB connection if it doesn't receive specific Xbox One GIP (Game Input Protocol) initialization packets.

**Symptoms:** USB device `20bc:5127` cycles connect/disconnect continuously; Bluetooth and USB-wired modes work fine.

## Fix

This package applies [Zixing Liu's patch](https://lore.kernel.org/linux-input/20260102030154.197749-2-liushuyu@aosc.io) to `xpad.c`, adding `FLAG_FORCE_INIT` which sends GIP acknowledge and announce packets during controller probing. The firmware recognizes these packets and stays in XINPUT mode.

The patch has been submitted upstream (v3, 2026-07-17) and is pending review. Once merged into the kernel, this DKMS package is no longer needed.

## Installation

### From AUR

```bash
yay -S xpad-beitong-dkms
# or
paru -S xpad-beitong-dkms
```

### From source

```bash
git clone https://github.com/675076143/xpad-beitong-dkms.git
cd xpad-beitong-dkms
makepkg -si
```

After installation, reboot or run:

```bash
sudo modprobe -r xpad && sudo modprobe xpad
```

## Requirements

- `dkms` package
- Kernel headers for your running kernel (e.g., `linux-headers`, `linux-zen-headers`, `linux-cachyos-rc-headers`, etc.)

## How it works

1. Copies `xpad.c` from the running kernel's headers
2. Applies the GIP init patch
3. Registers with DKMS for automatic rebuilds on kernel updates
4. Blacklists the in-kernel `xpad` module to ensure the patched one loads

## Compatible Devices

The following VID:PID combinations are recognized:

| VID | PID | Device |
|-----|-----|--------|
| 20bc | 5125-5128 | KP20A/KP40A |
| 20bc | 512f-5130 | KP70A |
| 20bc | 5133-5134 | KP50B |
| 20bc | 5145-5146 | KP40A/KP40B |
| 20bc | 5149-514a | KP50C |
| 20bc | 5150-5151 | KP50D |
| 20bc | 5152-5153 | KP50E |
| 20bc | 5154-5155 | KP40D |
| 20bc | 5158-5159 | KP20D |
| 20bc | 515b-515c | KP40D (White) |
| 20bc | 515d-515e | KP40F (White) |
| 20bc | 515f-5160 | KP70A |
| 20bc | 5169-516a | KP40F (Black) |

## Upstream Status

| Item | Status |
|------|--------|
| Patch author | Zixing Liu |
| Submitted | v3, 2026-07-17 |
| Target | Mainline Linux (expected 7.3 or later) |
| This DKMS | Deprecated after upstream merge |

## Links

- [Wiki page with full investigation log](https://github.com/675076143/notes/wiki/beitong-btp-kp40a-linux-usb-disconnect)
- [Upstream patch discussion (linux-input)](https://lore.kernel.org/linux-input/20260102030154.197749-2-liushuyu@aosc.io/)
- [Arch Wiki - Gamepad (ShanWan section)](https://wiki.archlinux.org/title/Gamepad)
