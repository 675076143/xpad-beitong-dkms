# Source provenance and review

## Official driver

- Repository: https://github.com/torvalds/linux
- Tag: v6.18; tag object `f7b88edb52c8dd01b7e576390d658ae6eef0e134` resolves to commit `7d0a66e4bb9081d75c82ec4957c50034cb0ea449`.
- Path: `drivers/input/joystick/xpad.c`.
- Immutable URL: https://raw.githubusercontent.com/torvalds/linux/7d0a66e4bb9081d75c82ec4957c50034cb0ea449/drivers/input/joystick/xpad.c
- Local file: `xpad-linux-6.18.c`, 81022 bytes.
- Git blob: `d72e89c25e5031cb4b9636258aff44cbed263137`, independently matched against the official repository's contents API using `git hash-object` on downloaded bytes.
- SHA-256: `6f37e6da9c5925b43447ae1a8bc34b7e159cbd8f0411467929ce124b17ca6311`.
- License: GPL-2.0-or-later, retained in the original file.

This verifies byte identity and pins integrity. It is not a local verification of the release tag's PGP signature. No upstream build scripts were downloaded or executed. Choosing a fixed older snapshot makes the package independent of the packaging host; it does not establish compatibility with arbitrary future kernels or include newer stock xpad improvements.

## Local GIP patch

The original repository base is `f4ce639f8f2e88ff3f8fbca75c3e5ce9b6857169`. Its `beitong-gip-init.patch`, attributed to Zixing Liu, was reviewed and rebased onto the pinned official driver. Packet bytes, original device list and GIP logic are retained. Context/line numbers changed. The pinned base lacks the original CachyOS source's `20bc` USB vendor match, so the standard Xbox 360 interface-class match for `20bc` is added explicitly. The two duplicate `5134`/`514a` name-only entries from the old source context are not duplicated. No new KP70C1 quirk is added.

Patch preparation failed initially on the device-table context of the original CachyOS-specific diff; the final rebased patch applies completely with `--fuzz=0`. This is why the exact source and patch are now paired and checksummed.

## Issue and PR decisions

- [PR #3](https://github.com/675076143/xpad-beitong-dkms/pull/3), head `2872f20c71ee8992c7f34fa323bb9d35da44bb63`: accepted the bug report that forced LLVM breaks GCC targets. Did not execute or merge its recipe. Removing LLVM alone breaks Clang targets, and its DKMS configuration still forces LLVM. The new common wrapper selects against target headers instead.
- [PR #4](https://github.com/675076143/xpad-beitong-dkms/pull/4), head `13ce1da110d3023ec16189dd03feedb5f44abae2`: accepted that headers may omit `.c` files. Did not execute its recipe. Replaced host-dependent fetching/search with a pinned local source, checksums and clean preparation. No network fallback is needed.
- [Issue #1](https://github.com/675076143/xpad-beitong-dkms/issues/1): reviewed the external EvernightFedora fork as text only. Reviewed blobs: `90-beitong-support.patch` (`3324f57f5d477c2d8942e2253ca0eb8b3410ecb8`), `90-beitong-support-rtm.patch` (`b552c13c3942eb38bf801da9a6b781d22f95b86c`), `95-betop-devid.patch` (`78121c0c9beb0b5cd2363778111b0d6252f44700`), `xpad-kp40d.patch` (`1748cd86097690f12fb098f6aa98a8d35bf2c688`), and `PKGBUILD` (`3fc7109feb46baf6be7fc22aa80d3338192265ac`). The fork contains both an older GIP approach and newer `FLAG_READ_XUSB10` vendor-descriptor handling. Its KP40D HID receiver match is `20dd:515c`, not evidence for `20dd:518b`. One patch removes an unrelated EasySMX ID; copyright preambles also warrant licensing clarification before reuse. No fork code was imported or executed.
- [Issue #2](https://github.com/675076143/xpad-beitong-dkms/issues/2): reporter's KP70C1 Mint is idle `20dd:518b`, active `20bc:518b`; adding an ID manually did not fix it. The fork's active `518b` entry opts into XUSB descriptor handling, a different mechanism from this GIP quirk. The issue alone does not justify applying either mechanism. Leave hardware support open; request active descriptors/logs and a controlled device test before proposing a separate device patch.

## Package lifecycle

The installed Arch/CachyOS DKMS 3.4.4 package provides `70-dkms-install.hook`, `70-dkms-upgrade.hook`, `71-dkms-remove.hook` and `/usr/share/libalpm/scripts/dkms`. Those hooks trigger on `/usr/src/*/dkms.conf` and handle lifecycle operations. The removed custom install script duplicated DKMS work, discarded errors and loaded/unloaded the live driver. The replacement has no install script or modprobe settings. Obsolete `CLEAN` and `REMAKE_INITRD` directives are omitted for current DKMS; manual `make clean` remains available via the same target-aware wrapper.
