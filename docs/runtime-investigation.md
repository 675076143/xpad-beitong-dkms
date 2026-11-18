# KP70 and reboot investigation (2026-11-18)

Tracks #1, #2, #7. No hardware support claim or runtime fix is made here.

## KP70 source and protocol boundary

External source: https://github.com/EvernightFedora/xpad-beitong-dkms
Reviewed head: 1bf39a52da45dc3b963ebc6804a3e0eb7c02562c.
`95-betop-devid.patch` associates 20bc:518a/b/c/d with FLAG_READ_XUSB10.
`90-beitong-support-rtm.patch` performs a device-recipient vendor IN control
request (bRequest=0xee, wValue=0, wIndex=4, length=40, timeout=25ms),
after usb_set_intfdata; it warns on error but does not inspect returned data.
Its HID receiver path only lists 20dd:515c, not issue #2's 20dd:518b.

This differs from our FLAG_FORCE_INIT path: Xbox One-style output packets
are prepared for selected Xbox360 devices. Our list does not include 518b.
Blindly combining both initialization sequences is not justified by either
report. A missing 518b ID is not the sole demonstrated failure mechanism.

Microsoft describes OS descriptors as vendor control transfers:
https://learn.microsoft.com/en-us/windows-hardware/drivers/usbcon/microsoft-os-1-0-descriptors-specification
That does not establish that request code 0xee is valid for this firmware,
that the returned compatible ID is XUSB10, or that the transfer switches mode.
Obtain the device's OS string/vendor code and a successful Windows USB capture
before implementing a narrowly scoped sequence. Do not replay arbitrary requests
against an active user's input device.

The external patch files explicitly say All rights Reserved, and repository
metadata supplies no license. Resolve the authors' permission/provenance before
copying their additions into GPL driver code; alternatively implement independently
from documented protocol and device captures. No external code is copied here.

## Reboot paths and actual evidence

Host inspection: kernel 7.3.4-1-cachyos, package 1.0-2.
`modinfo -F filename xpad`: updates/dkms/xpad.ko.zst.
Disk and live /sys/module/xpad/srcversion both: 681F4FB0DF7861374E9E9A1.
`modprobe --show-depends xpad` selects updates/dkms, with auto_poweroff=0.
This rules out a current disk/live srcversion mismatch; it does not reproduce
#5's contributor reboot failure or prove byte-identical loaded build IDs.

1.4 fixes unchecked/dynamic source, missing patch application in PR #5,
forced LLVM, old package-owned modules and stale DKMS state. Isolated lifecycle
evidence covers depmod selection/stock restoration, not boot image contents.
Installed Arch DKMS helper calls depmod after successful installs/removals.
Do not add a blanket module-load hook: it cannot replace an already loaded module.

/boot is unreadable to the current user; noninteractive sudo requires a password.
Thus boot image inclusion of old xpad remains unverified. No permission, boot
image, signing, initramfs or module changes were made. A blanket initramfs rebuild
would obscure the diagnosis and is not established as a required fix.

## Minimal next device observation

Run tools/collect-xpad-state.sh before and after one ordinary reboot with the
same controller mode, then reconnect once if it fails. Record buttons/axes and
whether reconnect restores operation. These distinguish kernel/installed-version
changes, disk/live module mismatch, USB mode/driver binding changes and a
reconnect-dependent device initialization failure. Do not change the driver
between observations. KP70 additionally needs both idle 20dd:518b and paired
20bc:518b descriptors and a successful initialization capture from that model.
The existing KP40 observations cannot substitute for KP70 hardware evidence.

## Diagnostic script review

The collector reports each missing/failed command explicitly and continues so an
unloaded module or absent package does not hide later evidence. USB output is
limited to Beitong 20bc/20dd device IDs and interface driver names via sysfs;
no serials, USB descriptor strings, unrelated devices, kernel logs or module
option values are emitted. USB enumeration can race unplugging; transient read
errors are reported. Running the collector does not read input events.

2026-11-18 follow-up: a 20bc:5127 KP40A is currently enumerated on this host;
no 518b KP70 is present in the observed USB list. KP40 evidence cannot validate
KP70. First collect a baseline without reconnecting; only ask the operator to
press one button and move one stick when input observation is actually ready.
Reboot comparison is a separate operator-controlled step, never automated here.
