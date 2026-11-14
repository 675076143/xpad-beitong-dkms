# Local validation — 2026-11-14

Isolated checkout: `/home/robin/Documents/Codex/2026-11-14/task/xpad-isolated`
Branch: `local/source-only-dkms`
Base: `f4ce639f8f2e88ff3f8fbca75c3e5ce9b6857169`
Evidence: `/home/robin/Documents/Codex/2026-11-14/task/xpad-validation/final`

## Completed

- `bash -n PKGBUILD dkms.conf`: pass.
- `python tests/test_package.py`: three tests pass, covering compiler selection from target config, DKMS's KERNELRELEASE argument, explicit LLVM/CC overrides, XPAD_LLVM priority, unknown-config rejection, explicit override with missing config, repeat prepare from clean source, deliberately corrupted source checksum rejection, and generated `.SRCINFO` equality.
- `makepkg --force`: exit 0, all five SHA-256 checks pass; no dependency checks skipped in the final run. No build function or network access is needed.
- Archive audit: precisely four package payload files under `/usr/src/xpad-beitong-1.1/` and three standard package metadata entries; no `.ko`, `.INSTALL` or modprobe configuration.
- Actual driver built directly with each target's installed headers and `KERNELRELEASE`, using the new Makefile wrapper. Both exit 0. Verbose compiler invocations are in `../xpad-validation/actual-clang.log` and `actual-gcc.log`.
- Final package extracted to an isolated staging tree. Actual DKMS 3.4.4 `add` and `build` run as the normal user with independent source/state/install/tmp trees. Both target builds exit 0 and status is `built` for both. The isolated install tree remains empty; `dkms install` was never run.

| Target | Header package | Compiler | Final DKMS module vermagic |
|---|---|---|---|
| 7.3.3-1-cachyos | linux-cachyos-headers 7.3.3-1 | Clang 23.1.4 | `7.3.3-1-cachyos SMP preempt mod_unload` |
| 6.18.60-2-cachyos-lts | linux-cachyos-lts-headers 6.18.60-2 | GCC 16.2.1 20260810 | `6.18.60-2-cachyos-lts SMP preempt mod_unload` |

The first target enables Clang ThinLTO; the second uses GCC with no LTO. Compiler and header package ownership were read with pacman. Tool versions: make 4.4.1-3.1; pacman 7.1.0.r9.g54d9411-6. DKMS's installed implementation independently appends LLVM=1 for the Clang target; the shared wrapper also selects correctly when called directly without that help.

## Reproduction and evidence

From the checkout, run:

```sh
python tests/validate_local.py /absolute/path/to/a-new-evidence-directory
```

This validates the package, extracts it locally and runs only isolated DKMS add/build/status. The destination must be new. It assumes the two documented headers, makepkg/fakeroot and DKMS are already installed. It does not install software, the package or modules. During this isolated test only, `try_sign_modules=false` is passed in the child environment, producing unsigned never-installed test outputs; no DKMS framework configuration or system signing settings are edited.

The final evidence directory includes every exact command, output and exit code in `*.log`, the extracted package under `stage`, and DKMS compiler logs under `state/xpad-beitong/1.1/<kernel>/x86_64/log/make.log`.

SHA-256 of final package `xpad-beitong-dkms-1.1-1-any.pkg.tar.zst`:
`7409f7bbbc1dbb582bc2a869929ff730f04f5b24be81e002544fad7eb384aa74`

Final isolated DKMS module hashes (local build evidence, not signed release artifacts):

- Clang target: `697ad26ad51ac7f4d9e21e2f261b0c9ff15d6c3c7973b35cc5bb28327b843d6c`
- GCC target: `73f65176e57a73265d6124901880a8a8db39e1aafa96995bb27ecf4da1c15e1f`

Unified patch context contains leading space before tabs by format; `git -c core.whitespace=-space-before-tab diff --check` passes. Patches themselves apply with zero fuzz.

## Preserved system and remaining coverage

The original dirty AUR checkout `/home/robin/.cache/yay/xpad-beitong-dkms` retains its preexisting `pkgrel` change and package/src/pkg files. No files there were edited. `/usr/src/xpad-beitong-1.0/xpad.c` and the original AUR `src/xpad.c` still share SHA-256 `666568a76d5ff17f4ca02e714c836453c40dfc5cca55e7b304b39118ff262bd2`. No installed driver, system module tree or system configuration was changed.

No root, DKMS install, depmod, module load/unload, controller interaction, push, merge, comment, release or AUR publication occurred. The external fork and contributor PR recipes were read as text; none were executed. The only downloaded executable-source input compiled here is the reviewed official pinned xpad source plus this repository's reviewed patch.

Compilation and package structure are validated; hardware operation, signatures/Secure Boot acceptance, package installation/removal transactions, official Arch linux-zen, other kernels/architectures and KP70C1 support are not. No full hardware or release-readiness claim is made. The source pin intentionally precedes newer stock-driver changes; extending compatibility requires review/rebase and testing. Device changes should remain separate from this packaging repair; issue #2 stays open pending evidence.
