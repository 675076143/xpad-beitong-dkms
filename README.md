# xpad-beitong-dkms

Source-only DKMS package for the existing Beitong KP-series GIP initialization workaround, based on Zixing Liu's patch. This is a local packaging repair candidate, not a claim of newly verified hardware support.

## Reproducible sources

`xpad-linux-6.18.c` is an unmodified, vendored copy of the official Linux v6.18 driver at commit `7d0a66e4bb9081d75c82ec4957c50034cb0ea449`. Every PKGBUILD input has a SHA-256 checksum. See [SOURCES.md](SOURCES.md) for provenance, review decisions and compatibility limits.

`prepare()` always copies the pinned source into a fresh `src/module` directory and applies the reviewed local patch with zero fuzz. It does not search installed headers for source or download anything. Headers need not contain `xpad.c`.

## Build and lifecycle

On Arch/CachyOS, install DKMS and headers matching each intended target kernel. Clang-built targets also need Clang, LLVM and LLD; GCC-built targets need the matching GCC/binutils toolchain. Kernel configuration determines which kernel features are compiled into the driver.

Build the package with `makepkg`. It contains only four files under `/usr/src/xpad-beitong-1.1/`: patched `xpad.c`, `Kbuild`, `Makefile` and `dkms.conf`. There is no host-specific `.ko`, custom `.install` hook or modprobe configuration.

Arch's DKMS pacman hooks handle registration, rebuild, installation and removal during package transactions. Failures remain visible. This package does not explicitly load, unload or reload a live module. Review the DKMS transaction output and reboot when ready to activate an installed build. No package or module was installed during this validation.

The Makefile wrapper reads the **target** `KDIR/.config`: `CONFIG_CC_IS_CLANG=y` selects `LLVM=1`, and `CONFIG_CC_IS_GCC=y` selects GCC. Unknown configuration fails explicitly. A separate `Kbuild` prevents DKMS's `KERNELRELEASE` argument from bypassing the wrapper. `KVER` defaults to the running kernel only for direct manual builds; DKMS supplies its own target header directory and release.

Explicit `LLVM=...` and command-line `CC=...` overrides are passed through. `XPAD_LLVM=...` takes precedence even over LLVM arguments appended by DKMS (empty means GCC). Overrides do not establish compatibility with a mismatched kernel toolchain.

## Validation

The actual patched driver compiles on these installed x86_64 targets:

| Target headers | Compiler selection | Validation |
|---|---|---|
| `7.3.3-1-cachyos` | Clang 23.1.4, LLVM, ThinLTO | Local compile |
| `6.18.60-2-cachyos-lts` | GCC 16.2.1, binutils | Local compile |

A fixed driver snapshot is not guaranteed compatible with every kernel version, configuration or architecture. Other targets need independent compile and device testing; build errors must not be bypassed. Older source may omit newer stock-driver fixes and devices. Review/rebase the pinned snapshot before extending support. See [VALIDATION.md](VALIDATION.md) for final results and commands.

Offline packaging/compiler-selection checks: `python tests/test_package.py`.

## Device status

The existing patch retains the original `20bc` IDs: `5125–5128`, `512f–5130`, `5133–5134`, `5145–5146`, `5149–514a`, `5150–5155`, `5158–5159`, `515b–5160` and `5169–516a`. Recognition and compilation are not hardware verification. The original project reported KP40A operation; this repair did not interact with a controller.

[Issue #2](https://github.com/675076143/xpad-beitong-dkms/issues/2) reports KP70C1 Mint as `20dd:518b` while idle and `20bc:518b` while active, and says manually adding the ID did not fix operation. KP70C1 remains **unverified**; no new quirk is enabled. The idle receiver is not assumed to be XInput. Useful next evidence is the active interface descriptors, kernel/driver logs and a separately approved hardware test comparing GIP initialization with XUSB descriptor handling. Do not infer support from an ID alone.

The external fork in [issue #1](https://github.com/675076143/xpad-beitong-dkms/issues/1) was reviewed as text only. Its newer XUSB/HID behavior was not imported. PRs [#3](https://github.com/675076143/xpad-beitong-dkms/pull/3) and [#4](https://github.com/675076143/xpad-beitong-dkms/pull/4) informed the packaging fixes; their recipes were not executed.
