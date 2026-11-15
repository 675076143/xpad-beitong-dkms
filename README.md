# xpad-beitong-dkms

Source-only DKMS package for the existing Beitong KP-series GIP initialization workaround, based on Zixing Liu's patch. This is a local packaging repair candidate, not a claim of newly verified hardware support.

## Release scope and sources

The earlier local candidate `9e626f4` compiled, but its Linux v6.18 snapshot missed fixes already present in both target releases, including a Share-button packet-length check. It must not be published as a general replacement for newer stock xpad.

This revision vendors **three exact stable snapshots**, byte-identical to their corresponding CachyOS release source files: Linux 7.3.3, 7.3.4 and 6.18.60. Each has its own zero-fuzz Beitong patch and SHA-256 checksums. DKMS selects the local prepatched source for its exact target; it does not download anything or fall back to an older snapshot. Both the Makefile and DKMS config reject unreviewed releases. See [SOURCES.md](SOURCES.md) and [RELEASE-REVIEW.md](RELEASE-REVIEW.md).

Allowed exact targets are `7.3.3-1-cachyos`, `7.3.4-1-cachyos`, `6.18.60-2-cachyos-lts`, official Arch `7.3.4-arch1-2`, and official linux-zen `7.3.4-zen2-2-zen`. Adding another target requires independently checking its stock xpad, preserving fixes, updating the source map and retesting. A later kernel upgrade will be skipped rather than silently built from an older driver.

## Build and lifecycle

On Arch/CachyOS, install DKMS and headers matching each intended target kernel. Clang-built targets also need Clang, LLVM and LLD; GCC-built targets need the matching GCC/binutils toolchain. Kernel configuration determines which kernel features are compiled into the driver.

Build the package with `makepkg`. It contains only seven files under `/usr/src/xpad-beitong-1.4/`: three prepatched snapshots in `sources/`, `Kbuild`, `Makefile`, `dkms.conf` and the pinned source/attribution record `SOURCES.md`. There is no host-specific `.ko`, custom `.install` hook or modprobe configuration.

Arch's DKMS pacman hooks handle registration, rebuild, installation and removal during package transactions. Failures remain visible. This package does not explicitly load, unload or reload a live module. Review the DKMS transaction output and reboot when ready to activate an installed build. No package or module was installed during this validation.

The Makefile wrapper reads the **target** `KDIR/.config`: `CONFIG_CC_IS_CLANG=y` selects `LLVM=1`, and `CONFIG_CC_IS_GCC=y` selects GCC. Unknown configuration fails explicitly. `KVER` must be an allowed release and match the target header release. A separate `Kbuild` prevents DKMS's `KERNELRELEASE` argument from bypassing the wrapper. `KVER` defaults to the running kernel only for direct manual builds; DKMS supplies its own target header directory and release.

Explicit `LLVM=...` and command-line `CC=...` overrides are passed through. `XPAD_LLVM=...` takes precedence even over LLVM arguments appended by DKMS (empty means GCC). Overrides do not establish compatibility with a mismatched kernel toolchain.

## Validation

Current and prior scoped x86_64 build evidence:

| Target headers | Compiler selection | Validation |
|---|---|---|
| `7.3.3-1-cachyos` | Clang 23.1.4, LLVM, ThinLTO | Prior 1.2 compile; headers no longer installed |
| `7.3.4-1-cachyos` | Clang 23.1.5, LLVM, ThinLTO | Current isolated DKMS build; kernel used 23.1.4 |
| `6.18.60-2-cachyos-lts` | GCC 16.2.1, binutils | Actual controlled package transactions |
| `7.3.4-arch1-2` | GCC 16.2.1, binutils | Signed official inputs; actual transactions and legacy upgrade |
| `7.3.4-zen2-2-zen` | GCC 16.2.1, binutils | Signed official inputs; actual transactions and legacy upgrade |

Other target releases are intentionally rejected. Matching header release names do not establish compatibility with arbitrary custom source changes or architectures; independent source review, compilation and device testing remain necessary. See [VALIDATION-7.3.4.md](VALIDATION-7.3.4.md) for current results/commands and [VALIDATION.md](VALIDATION.md) for historical 1.2 evidence.

Offline packaging/compiler-selection checks: `python tests/test_package.py`.

## Device status

The existing patch retains the original `20bc` IDs: `5125–5128`, `512f–5130`, `5133–5134`, `5145–5146`, `5149–514a`, `5150–5155`, `5158–5159`, `515b–5160` and `5169–516a`. Recognition and compilation are not hardware verification. The original project reported KP40A operation; this repair did not interact with a controller.

[Issue #2](https://github.com/675076143/xpad-beitong-dkms/issues/2) reports KP70C1 Mint as `20dd:518b` while idle and `20bc:518b` while active, and says manually adding the ID did not fix operation. KP70C1 remains **unverified**; no new quirk is enabled. The idle receiver is not assumed to be XInput. Useful next evidence is the active interface descriptors, kernel/driver logs and a separately approved hardware test comparing GIP initialization with XUSB descriptor handling. Do not infer support from an ID alone.

The external fork in [issue #1](https://github.com/675076143/xpad-beitong-dkms/issues/1) was reviewed as text only. Its newer XUSB/HID behavior was not imported. PRs [#3](https://github.com/675076143/xpad-beitong-dkms/pull/3) and [#4](https://github.com/675076143/xpad-beitong-dkms/pull/4) informed the packaging fixes; their recipes were not executed.

A practical, unexecuted reporter plan is available in [KP70C1-VALIDATION.md](KP70C1-VALIDATION.md). Publication remains blocked on the release gates in [RELEASE-REVIEW.md](RELEASE-REVIEW.md).

Current official Arch/linux-zen targets and the reviewed legacy 1.0-1 migration have now passed isolated transactions. See [ARCH-RELEASE-VALIDATION.md](ARCH-RELEASE-VALIDATION.md) for signatures, exact scope, fingerprints, remaining runtime/signing boundaries and the unexecuted AUR publication plan. Unknown releases remain refused; do not expect a working Beitong workaround on unlisted kernels.
