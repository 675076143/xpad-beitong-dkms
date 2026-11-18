# KP70C1 Mint reporter validation plan

This is an unexecuted plan for a willing reporter, not a support claim or instructions to install a test driver. Issue #2 describes the **controller's Mint edition**, not an established Linux distribution. Collect the actual OS/kernel first. The new packaging candidate does not enable a `518b` quirk.

## Baseline without changing drivers

Record kernel release, distribution, controller model/firmware if known, selected connection mode, receiver firmware if known, and which driver package is installed. Read-only commands, if already available:

```sh
uname -r
cat /etc/os-release
dkms status
modinfo -n xpad
modinfo -F vermagic xpad
cat /sys/module/xpad/srcversion
cat /proc/bus/input/devices
lsusb
lsusb -t
```

`modinfo` shows the on-disk module selected for a kernel; it does not prove the running module is that file. `/sys/module/xpad` may not exist if it is not loaded. Record this instead of loading it. A difference between on-disk and running srcversion may indicate an older loaded build. Do not unload/reload, bind/unbind, write `new_id`, blacklist drivers or change power settings during baseline collection. No extra software needs to be installed just to fill a missing field.

## Activation and USB interfaces

With the reporter's consent to normal controller use, observe these states on the same USB port: receiver plugged in with controller off; controller on/paired; controller off again. Note timestamps and whether the bus/device number or ID changes. Do not treat `20dd:518b` as an Xbox controller merely because it is the idle receiver ID.

Record `lsusb`, `lsusb -t`, relevant kernel journal messages, and, where permissions permit, full standard descriptors for the observed ID:

```sh
lsusb -v -d 20dd:518b
lsusb -v -d 20bc:518b
```

These commands belong on the reporter's machine only; they were not run against Robin's controller. Descriptor output may contain serial numbers; remove personal serials before sharing. If descriptor/journal access is denied, report that limitation rather than changing permissions. Do not send handcrafted USB control messages.

For each **interface**, record class, subclass, protocol, number of endpoints, endpoint transfer types/directions and bound driver. `bDeviceClass` alone is insufficient on composite devices. The reviewed stock xpad's `20bc` Xbox 360 vendor match requires interface class `0xff`, subclass `0x5d` (decimal 93), and protocol `0x01` or `0x81` (decimal 129). Probe also requires exactly two endpoints with one interrupt IN and one interrupt OUT. Other layouts need separate analysis rather than a forced match. In stock xpad, an unknown device with protocol 129 takes the Xbox 360 wireless parser; a name/ID-only entry can affect classification, so record what the reporter actually changed when manually adding the ID.

The sysfs interface `driver` symlink and `modalias` provide binding evidence without writes. After identifying the exact USB port/interface from `lsusb -t`, read only that interface, for example:

```sh
readlink -f /sys/bus/usb/devices/<observed-interface>/driver
cat /sys/bus/usb/devices/<observed-interface>/modalias
```

Replace the placeholder with an observed interface such as `1-3:1.0`; do not paste it literally or guess another device. An idle HID interface bound to `usbhid` is a separate path, not evidence that it should be forced into xpad. The external fork's extra HID handler targets `20dd:515c`, not `518b`.

## Binding, events and reconnect observations

Keep a timestamped kernel log covering activation and a few minutes of normal use (journalctl/dmesg if permitted). Record whether active `20bc:518b` stays enumerated, whether xpad binds, and whether the expected `/dev/input/event*` node appears. Distinguish these failure stages:

| Observation | Next question |
|---|---|
| No transition out of idle `20dd` | Is pairing/mode/receiver activation occurring? No xpad assumption yet. |
| Active ID, different interface descriptors | Does this device speak the protocol that xpad expects? |
| Matching interface, no xpad binding | Is the module present/selected, and does probe report an error? |
| xpad bound, no input node | Does input initialization fail in the kernel log? |
| Input node exists, no events | Check actual packet/parser path before inventing an initialization quirk. |
| Repeated USB disconnect/reset | Preserve timestamps and enumeration IDs; classify separately from app mapping issues. |
| Input events normal, one application fails | Investigate application/SDL mapping separately. |

If an input event viewer is already installed and the reporter can access the specific gamepad event node, observe it **without grabbing the device**. Record name, VID/PID and capabilities; test face buttons, both sticks, D-pad, triggers, shoulders, Start/Select and guide/share where present. Capture whether D-pad is axes or buttons and whether events stop after a reconnect. Do not select a keyboard or unrelated device. Rumble testing actively sends device output and belongs to a later separately agreed test, not this baseline.

After baseline activation, the reporter can choose to test several normal power-off/on and receiver unplug/replug cycles. Record whether each cycle re-enumerates, binds and restores events without module manipulation. Re-check event-node identity after every cycle rather than reusing a stale node. Suspend/resume is optional and separate; do not disrupt an active session to gather it.

## Only then consider a separate experimental device patch

The existing project uses forced GIP initialization for known IDs. The external fork's newer `20bc:518b` entry instead selects a Microsoft XUSB feature-descriptor request (`bRequest=0xee`, index 4). Their mechanisms are different; neither is justified solely by a USB ID, and issue #2 explicitly says an ID-only edit failed. Generic Xbox One GIP support already present in stock xpad is not the Beitong force-init quirk.

A maintainer should first review the baseline descriptors/logs, then propose one small experiment at a time against the reporter's exact stock source: baseline, a separately justified GIP candidate, or a separately reviewed XUSB candidate. Preserve unrelated stock fixes and provide the precise source/patch hashes and rollback plan. Any install/module switching or USB capture/control traffic requires a separate approved hardware session; none is performed here. Successful compilation alone is not device support.

Success evidence would include stable active enumeration, correct binding, expected event capabilities and usable controls, and repeated reconnect recovery for that exact device/firmware/kernel. Keep KP70C1 support unverified until that evidence exists.
