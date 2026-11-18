# Exact CachyOS 7.3.4 extension — 2026-11-15

Independent worktree: `/home/robin/Documents/Codex/2026-11-14/task/xpad-7.3.4`
Branch: `local/cachyos-7.3.4`
Base preserved: `5b0cb179f3c55f54e3ff917d5ddaa8ae81bd738e`
Evidence: `/home/robin/Documents/Codex/2026-11-14/task/xpad-validation/7.3.4/`

## Source and target verification

- Running target and installed headers release: `7.3.4-1-cachyos`; both header `version` and `include/config/kernel.release` agree.
- Header Makefile owned by `linux-cachyos-headers 7.3.4-1`, x86_64_v4; pacman records signature validation. Header config selects Clang, LLD and Clang ThinLTO, and records `clang version 23.1.4`.
- Current installed compiler is Clang 23.1.5 (`clang 23.1.5-2`). Actual build emits the expected compiler-version warning, preserved in its log; it still exits 0. No compiler or package was installed to suppress it.
- CachyOS source tag `cachyos-7.3.4-1` resolves to `779ca9af71579431ca932a13a7c2ed5934b289ad`; official stable v7.3.4 resolves to `7595a62d45ee1a2297eafa5f2ef5d0a45142d84d`. Both xpad files have Git blob `d2eb48d98fead7d89eb3e45613a52176c4fa5fad` and SHA-256 `d3d9500cac4a59aad0a6bfe1d064e5a4c16cfc18d928f4bf6f69f6fd51511176`.
- `git hash-object` on retrieved bytes matches both API blob IDs, and byte comparison agrees. GitHub reports valid release-tag signatures; no local PGP verification or installed-binary source reconstruction is claimed. Generic CachyOS recipe revision/source mapping is recorded in SOURCES.md; installed packages are the znver4 variants.
- Full xpad 7.3.3 → 7.3.4 diff is one added GameSir `3537:1040` row. No code is removed, no Beitong quirk has landed. That stock row and all stock fixes are retained.

## Minimal extension

Add an exact 7.3.4 snapshot and rebased copy of the existing reviewed repository GIP patch; add only `7.3.4-1-cachyos` to the source map and DKMS allowlist. Prior 7.3.3 and 6.18.60 snapshots/patches are byte-unchanged. No external fork code or contributor recipe is executed. Bump the local candidate identity to 1.3 so changed source is not confused with cached DKMS 1.2 state; no version has been published.

The package remains source-only: three prepatched local snapshots, Makefile, Kbuild and dkms.conf under `/usr/src/xpad-beitong-1.3/`. No `.ko`, `.INSTALL`, module-loader script, custom pacman hook or network fetch. Unknown releases still fail closed.

## Actual results

`python tests/validate_local.py <new-evidence-dir> 7.3.4-1-cachyos 6.18.60-2-cachyos-lts` completed:

| Check | Result |
|---|---|
| Three offline test methods | Pass, including selection for all three known releases and unknown/mismatched-target rejection |
| Shell syntax / generated .SRCINFO consistency | Pass |
| makepkg, all nine SHA-256 inputs | Exit 0; all pass; normal dependency checks |
| Archive payload whitelist | Pass; six source/config files, no prebuilt module or scriptlet |
| Isolated DKMS 3.4.5 add/build/status | Exit 0; two requested targets `built` |
| 7.3.4 actual patched driver | `7.3.4-1-cachyos SMP preempt mod_unload` vermagic; exit 0 |
| LTS actual patched driver, GCC 16.2.1 | `6.18.60-2-cachyos-lts SMP preempt mod_unload` vermagic; exit 0 |
| Unreviewed 7.3.5 DKMS build request | Exit 77 before compilation |
| Isolated installation tree | Empty |

7.3.3 headers are no longer installed, so **no new real 7.3.3 compile was performed**. Its target remains enabled with the original exact source and previous 1.2 build evidence; unit tests still cover its mapping. The full test script defaults to all three and requires their headers; explicit arguments above reproduce precisely this run.

Reproduce from this worktree using an unused evidence-directory path:

```sh
python tests/validate_local.py /absolute/new/evidence-dir 7.3.4-1-cachyos 6.18.60-2-cachyos-lts
```

The script uses only installed trusted tools, local reviewed source and isolated DKMS source/state/install/tmp paths. Exact commands and exit codes are in `final/*.log`; compiler logs are in `final/state/xpad-beitong/1.3/<release>/x86_64/log/make.log`. Only isolated test processes use `try_sign_modules=false`; host signing configuration is not changed and test modules are unsigned.

Local package SHA-256 (`xpad-beitong-dkms-1.3-1-any.pkg.tar.zst`): `a522456632d9d37e716c67056a48e162dbc9ab9b21bccca05a8b821146ac3cbe`.

Actual isolated module SHA-256:

- 7.3.4: `3dfe0117326024f8f5c49ae5804e6b4a7cd13df112759cc64e36dd3115713b09`
- LTS: `97038ad68d3a61ca142b9bf15b0bb4f31afcaddbd0d13b977c3663f17d149aa1`

## Boundaries still open

No pacman install/upgrade/remove, DKMS install/remove, depmod, module load/unload/reload, physical controller operation, signing-policy change, root/sudo, GitHub/AUR mutation or publication occurred. The installed driver and original cache pkgrel=2 edit were left unchanged. The original worktree remains at 5b0cb17.

Field KP40A observations were of **running DKMS 1.0**, not this candidate. Real isolated lifecycle/legacy-migration and signing acceptance, followed by separately authorized candidate installation and physical button/axis/reconnect testing, remain required before release. A successful compile and matching vermagic do not establish runtime or hardware safety. KP70C1 support remains unverified and unchanged.
