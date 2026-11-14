# Local validation — exact-release candidate, 2026-11-14

Checkout: `/home/robin/Documents/Codex/2026-11-14/task/xpad-isolated`
Branch: `local/release-source-review`
Preserved previous commit: `9e626f4b9245a6399e96e3820ebb8b7d225b621a`
Final evidence directory: `/home/robin/Documents/Codex/2026-11-14/task/xpad-validation/release-candidate`

The earlier v6.18 candidate's results remain in `../xpad-validation/final`; they do not establish release suitability. This revision packages per-target sources as documented in [SOURCES.md](SOURCES.md). Publication gates remain in [RELEASE-REVIEW.md](RELEASE-REVIEW.md).

## Completed results

- Shell syntax: `bash -n PKGBUILD dkms.conf`, pass.
- Three offline tests pass: exact source/compiler selection including DKMS KERNELRELEASE; explicit LLVM, CC and XPAD_LLVM overrides; unknown/mismatched target and config rejection; repeated preparation; preserved stock device IDs and Share-button length checks; deliberate checksum corruption rejection; `.SRCINFO` and DKMS allowlist consistency.
- `makepkg --force`: exit 0, all seven input checksums pass, normal dependency checks pass. No build function or download is needed.
- Archive audit: exactly five payload files, all under `/usr/src/xpad-beitong-1.2/`: two prepatched snapshots in `sources/`, plus `Makefile`, `Kbuild`, `dkms.conf`. No `.ko`, `.INSTALL` or modprobe configuration.
- Actual driver builds through DKMS 3.4.4 in isolated source/state/install/tmp directories, as the normal user. Add/build/status exit 0. Separate Kbuild ensures DKMS's KERNELRELEASE does not bypass the source/compiler wrapper.

| Target | Source baseline | Compiler | DKMS state / vermagic |
|---|---|---|---|
| `7.3.3-1-cachyos` | Official 7.3.3 = CachyOS source tag | Clang 23.1.4, ThinLTO | built / `7.3.3-1-cachyos SMP preempt mod_unload` |
| `6.18.60-2-cachyos-lts` | Official 6.18.60 = CachyOS source tag | GCC 16.2.1 20260810 | built / `6.18.60-2-cachyos-lts SMP preempt mod_unload` |

Headers are owned by `linux-cachyos-headers 7.3.3-1` and `linux-cachyos-lts-headers 6.18.60-2`. Both installed target configurations and package provenance were read; header/source paths are explicit. Actual unsupported DKMS build for `7.3.4-1-cachyos` rejects via BUILD_EXCLUSIVE with exit 77 before compiling; see `unsupported.log`.

The isolated install directory is empty. No `dkms install`, depmod, module load/unload, package install, controller interaction or system-configuration change occurred. During test DKMS processes only, `try_sign_modules=false` prevents signing/creating keys for never-installed test outputs; no system policy was edited.

## Reproduction

From this checkout:

```sh
python tests/test_package.py
python tests/validate_local.py /absolute/path/to/a-new-evidence-directory
```

The full script requires the already-installed two headers, makepkg/fakeroot and DKMS. It builds the local package, audits/extracts it and runs only isolated DKMS add/build/status. It never installs software or modules. Use a new evidence directory. Exact executed commands, outputs and exit codes are in `*.log`; actual compiler build logs are under `state/xpad-beitong/1.2/<kernel>/x86_64/log/make.log`.

Local package SHA-256 (`xpad-beitong-dkms-1.2-1-any.pkg.tar.zst`):
`e365401e13b55381b9b8aaf848d5fd7ae3e8ffc0d446f00351c08265d3578f5c`

Local module SHA-256 (unsigned build evidence, not release artifacts):

- 7.3.3: `447a3249e3c10471aaef73a3cdda76b307da0228bcab301230d76b19d8ff7185`
- 6.18.60: `394ab7a795b14280b7f9e73beecd7d5b57b869815f2ddef6276aff812b1c5fa6`

Both patches apply at zero fuzz. `git -c core.whitespace=-space-before-tab,-blank-at-eol diff --check` excludes unified-patch context indentation and blank context lines. Those literal context lines are required by the patch format; the source bytes are preserved. Full source comparisons include a missed bounds check and other changes; see RELEASE-REVIEW.md.

## Preserved environment and limits

The dirty original AUR checkout `/home/robin/.cache/yay/xpad-beitong-dkms`, installed `/usr/src/xpad-beitong-1.0`, and all system configuration remain untouched. Installed and original AUR `src/xpad.c` still hash to `666568a76d5ff17f4ca02e714c836453c40dfc5cca55e7b304b39118ff262bd2`.

No contributor recipe or external fork code was executed. The only driver code compiled is the reviewed official exact-release source plus the reviewed repository GIP patch. No root, push, merge, GitHub comment, release or AUR publication occurred. Tests do not establish hardware behavior, installation lifecycle or signed-module acceptance; KP70C1 support remains unverified.
