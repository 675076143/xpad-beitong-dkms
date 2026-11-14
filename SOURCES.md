# Source provenance and review

## Current exact-release snapshots

Both vendored files are unmodified official stable sources and byte-identical to the corresponding CachyOS source-tag file. The package prepares a clean, separately patched copy of each. No package/DKMS build downloads source.

| File | Official stable commit | CachyOS source tag / commit | Git blob | SHA-256 |
|---|---|---|---|---|
| `xpad-linux-7.3.3.c` | `d50d994bffa3c7c6db2d8bc4c5f0c55e3f46b0cd` | `cachyos-7.3.3-1` / `1d4761de576fb0c50f9b9646c276811a67a173ad` | `810e52782ae891f3273598474b66ac89db13a6c8` | `b47281151829fc382c4bcb5f466865f476a6f4ebfacd617ee49393f99c1e3950` |
| `xpad-linux-6.18.60.c` | `f45ed76d6791cf72ff1265ee93511175bbbc2f18` | `cachyos-6.18.60-1` / `d98939f3daa1a8553dbea002aab392c970c9a7a7` | `126f99cd0b29ea23099a24cac3aebe63aab1dcf1` | `a82cdcd930f7e9528ca645d68ade181531d2ac4de1e3e8395e7935945a3bb92e` |

For each commit the path is `drivers/input/joystick/xpad.c` in `gregkh/linux` or `CachyOS/linux`. Immutable references:

- [Official 7.3.3 source](https://github.com/gregkh/linux/blob/d50d994bffa3c7c6db2d8bc4c5f0c55e3f46b0cd/drivers/input/joystick/xpad.c)
- [CachyOS 7.3.3 source](https://github.com/CachyOS/linux/blob/1d4761de576fb0c50f9b9646c276811a67a173ad/drivers/input/joystick/xpad.c)
- [Official 6.18.60 source](https://github.com/gregkh/linux/blob/f45ed76d6791cf72ff1265ee93511175bbbc2f18/drivers/input/joystick/xpad.c)
- [CachyOS 6.18.60 source](https://github.com/CachyOS/linux/blob/d98939f3daa1a8553dbea002aab392c970c9a7a7/drivers/input/joystick/xpad.c)

Local `git hash-object` matches all four independently fetched file responses. GitHub reports valid signatures on all four release-tag objects; this is server-reported verification, not local GPG verification. GPL-2.0-or-later identifiers remain intact. No upstream/fork build scripts were executed.

The read-only CachyOS package recipes map installed version `7.3.3-1` to source tag `cachyos-7.3.3-1`, and `6.18.60-2` to source tag `cachyos-6.18.60-1` (`pkgrel=2` is not the source tag suffix). Recipe revisions reviewed: `6d02fae52812f9c836abffb4a5320aee9e07a294` and `3473896702e3579493c7fa5aac17d797dd392e89`, respectively, in `CachyOS/linux-cachyos`. Their original blobs are `9f53eefe72cc7d52f763841388669388170dff4b` and `fe9c5b1de8bed18dd6730c5de79f866696790ec2`. Installed packages are the znver4 variants; their cached `.BUILDINFO` hashes differ from the generic recipes, so this review does not claim a cryptographic reconstruction of the installed binary from the generic recipe. It establishes exact released source identity, not decompilation of installed modules.

## Why the earlier source strategy was rejected

Commit `9e626f4` is preserved. It pinned official Linux v6.18 (`7d0a66e4bb9081d75c82ec4957c50034cb0ea449`, blob `d72e89c25e5031cb4b9636258aff44cbed263137`), which compiled on both headers but predates stock fixes. Both reviewed releases add a Share-button report-length check before `data[len - offset]`, correct PDP `0e6f:0147` from Xbox One to Xbox 360, and add 23 device IDs. The 7.3.3 file also has RedOctane vendor matching and `kzalloc_obj` conversions. Compilation cannot detect these semantic regressions. That package must not replace newer stock xpad generally.

## Local patches and target selection

Repository base: `f4ce639f8f2e88ff3f8fbca75c3e5ce9b6857169`. Its GIP patch is attributed to Zixing Liu. The two `beitong-linux-*.patch` files rebase only that reviewed repository's packet bytes, original 28-device quirk list and GIP logic onto each exact stock snapshot. The stock `5134` and `514a` entries are replaced by flagged entries rather than duplicated. Existing `20bc` USB interface matching is retained; no extra vendor match, KP70C1 quirk, XUSB request or HID receiver driver is added. All stock device IDs and packet-length protection remain.

DKMS's regex and Makefile's source map permit only `7.3.3-1-cachyos` and `6.18.60-2-cachyos-lts`. The wrapper verifies the header release equals KVER before copying the matching local source to `xpad.c`; unknown or mismatched targets fail. There is no download, glob-based source search, major-version fallback or old source default. Header configuration still selects compiler, with explicit overrides retained. A future target needs a new source review and build, not just a widened regex.

## Issue and PR decisions

- [PR #3](https://github.com/675076143/xpad-beitong-dkms/pull/3), head `2872f20c71ee8992c7f34fa323bb9d35da44bb63`: accepted the bug report that forced LLVM breaks GCC targets. Did not execute or merge its recipe. Removing LLVM alone breaks Clang targets, and its DKMS configuration still forces LLVM. The new common wrapper selects against target headers instead.
- [PR #4](https://github.com/675076143/xpad-beitong-dkms/pull/4), head `13ce1da110d3023ec16189dd03feedb5f44abae2`: accepted that headers may omit `.c` files. Did not execute its recipe. Replaced host-dependent fetching/search with a pinned local source, checksums and clean preparation. No network fallback is needed.
- [Issue #1](https://github.com/675076143/xpad-beitong-dkms/issues/1): reviewed the external EvernightFedora fork as text only. Reviewed blobs: `90-beitong-support.patch` (`3324f57f5d477c2d8942e2253ca0eb8b3410ecb8`), `90-beitong-support-rtm.patch` (`b552c13c3942eb38bf801da9a6b781d22f95b86c`), `95-betop-devid.patch` (`78121c0c9beb0b5cd2363778111b0d6252f44700`), `xpad-kp40d.patch` (`1748cd86097690f12fb098f6aa98a8d35bf2c688`), and `PKGBUILD` (`3fc7109feb46baf6be7fc22aa80d3338192265ac`). The fork contains both an older GIP approach and newer `FLAG_READ_XUSB10` vendor-descriptor handling. Its KP40D HID receiver match is `20dd:515c`, not evidence for `20dd:518b`. One patch removes an unrelated EasySMX ID; copyright preambles also warrant licensing clarification before reuse. No fork code was imported or executed.
- [Issue #2](https://github.com/675076143/xpad-beitong-dkms/issues/2): reporter's KP70C1 Mint is idle `20dd:518b`, active `20bc:518b`; adding an ID manually did not fix it. The fork's active `518b` entry opts into XUSB descriptor handling, a different mechanism from this GIP quirk. The issue alone does not justify applying either mechanism. Leave hardware support open; request active descriptors/logs and a controlled device test before proposing a separate device patch.

## Package lifecycle

The installed Arch/CachyOS DKMS 3.4.4 package provides `70-dkms-install.hook`, `70-dkms-upgrade.hook`, `71-dkms-remove.hook` and `/usr/share/libalpm/scripts/dkms`. Those hooks trigger on `/usr/src/*/dkms.conf` and handle lifecycle operations. The removed custom install script duplicated DKMS work, discarded errors and loaded/unloaded the live driver. The replacement has no install script or modprobe settings. Obsolete `CLEAN` and `REMAKE_INITRD` directives are omitted for current DKMS; manual `make clean` remains available via the same target-aware wrapper.
