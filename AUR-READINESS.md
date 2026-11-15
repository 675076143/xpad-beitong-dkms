> Historical assessment from earlier candidates. Current signed official-Arch inputs and legacy transaction results supersede the listed Arch/migration gaps; see [ARCH-RELEASE-VALIDATION.md](ARCH-RELEASE-VALIDATION.md). Authentication, production runtime/signing and publication remain unverified.

# AUR release review — 2026-11-15

**Do not replace the generic AUR package with this candidate yet.** Public AUR existence is now verified and controlled candidate lifecycle tests pass, but the candidate intentionally excludes official Arch/linux-zen. CachyOS GCC evidence does not establish official Arch support. The requested AUR publication acceptance is not achieved.

## Verified publication target, without authentication

- Public package: https://aur.archlinux.org/packages/xpad-beitong-dkms
- Public RPC evidence: https://aur.archlinux.org/rpc/v5/info?arg%5B%5D=xpad-beitong-dkms
- Public read-only Git: `https://aur.archlinux.org/xpad-beitong-dkms.git`
- RPC currently reports version **1.0-1**, maintainer and submitter **Robin6750**, upstream `https://github.com/675076143/xpad-beitong-dkms`.
- Anonymous `git ls-remote` advertises HEAD and `refs/heads/master` at `e3e25ce5d8063226a08580427fc1331f80284167`, matching the existing cache's committed HEAD. Therefore the committed cached recipe/.SRCINFO are anchored to the actual currently advertised remote, not merely a stale local guess.
- The public account-profile request returned HTTP 401 and was stopped; no login, keys, credentials or account modifications were attempted. A matching maintainer handle/upstream URL does not prove authenticated AUR write permission. That must be established before any future publication.

The original `/home/robin/.cache/yay/xpad-beitong-dkms` remains on master with its preexisting local `pkgrel=2` edit and artifacts untouched. No fetch/reset/commit was performed there. Version comparison confirms candidate `1.3-1` is greater than both public `1.0-1` and local `1.0-2`.

## Candidate and PR provenance

This worktree starts at `92656f9067ec6cbd0c70508814b603754018642a`. Driver sources, patches, Makefile, Kbuild and DKMS behavior remain unchanged. The small packaging supplement includes `SOURCES.md` as a checksummed input and installed source-directory text, so pinned source provenance and Zixing Liu's attribution survive standalone source/package distribution. There are now ten checksummed inputs and seven text/source payload files. No scriptlet, precompiled module or extra lifecycle owner is added. GPL-2.0-or-later matches all three official source SPDX headers.

Current PR reads confirm:

| PR | Exact head | Status and disposition |
|---|---|---|
| #3 | `2872f20c71ee8992c7f34fa323bb9d35da44bb63` | Open, unmerged. Bug report credited; raw change does not fix target selection/DKMS or general lifecycle. |
| #4 | `13ce1da110d3023ec16189dd03feedb5f44abae2` | Open, unmerged. Bug report credited; host-dependent unchecked source acquisition is replaced independently, not executed. |

Both have base `f4ce639f8f2e88ff3f8fbca75c3e5ce9b6857169`. No contributor recipe was executed, no PR was merged/commented on, and no repeated thank-you was posted. Their bug reports are not evidence that the independent implementation is verified on official Arch.

The official stable/CachyOS snapshots are publicly addressable by immutable commits in SOURCES.md. The source archive is self-contained: PKGBUILD, .SRCINFO, all local source/patch inputs and SOURCES.md. Every archived input matches its SHA-256; generated .SRCINFO matches semantically (makepkg adds timestamp comments). This is pinned source integrity, not a claim of bit-identical tarballs or locally verified upstream PGP signatures.

## Completed actual tests

Evidence root: `/home/robin/Documents/Codex/2026-11-14/task/xpad-validation/aur-release/`.

- Clean worktree package build and source-archive build pass with normal dependency checks. Three offline tests pass; .SRCINFO, target mapping, repeat preparation, checksum-corruption rejection and stock fix/ID preservation remain covered.
- Both archives contain the source/attribution record. The package has no `.INSTALL`, `.ko`, custom pacman hook or module-loader script. It owns only its versioned `/usr/src` subtree plus package metadata.
- Real pacman install, same-source pkgrel upgrade `1.3-1 -> 1.3-2`, candidate source-version-directory upgrade `1.3 -> 1.4`, and remove all pass in a controlled bubblewrap root. The latter two versions are self-authored test fixtures using the same reviewed code, not proposed public releases.
- Actual unmodified installed Arch DKMS helper and its three standard hooks run. DKMS installs for `7.3.4-1-cachyos` and `6.18.60-2-cachyos-lts`; status and vermagic are checked after each install/upgrade. Source-version upgrade removes the old source/state directory. Removal unregisters DKMS and restores both seeded stock module files byte-for-byte. No module-loader/signing stub was called.

### Exact isolation and limits

Bubblewrap creates independent user, mount, PID and network namespaces; namespace UID/GID 0 maps only to host UID/GID 1000. Host `/usr` and target headers are read-only. Source/module/state/package DB/log writes are bound only to workspace fixture paths. Host `/etc`, `/var`, `/home`, `/sys` and input devices are not exposed; CAP_SYS_MODULE is dropped and loader commands are intercepted. The network namespace has only loopback. No sudo or host kernel/security setting is changed.

The fixture copies existing package metadata except the old xpad package and uses the already installed trusted tools/dependencies. It permits unsigned local test archives and disables module signing **only in its own config**. This tests the unsigned isolated policy, not Secure Boot/signature acceptance. It exposes only the three standard DKMS hooks; host-specific initramfs/boot integration is not tested.

The first real transaction returned pacman exit 0 while its inner network sandbox refused the hook. That failure is retained under `lifecycle/evidence/attempt1`. A fixture-only `DisableSandboxNetwork` avoids redundant inner isolation; the outer bubblewrap network namespace remains enforced. The successful retry is actual transaction evidence, but does not prove default nested-pacman sandbox compatibility. A previous read-only Docker inventory command was in fact a Podman shim that attempted runtime repair and hit read-only protection; that path was stopped, and the existing pause-file timestamps remained unchanged. No container engine was used for the successful tests.

Original online/cached 1.0 `.INSTALL` scripts and old binary payload migration were **not executed/tested**. The candidate-to-candidate source-version test is not a substitute for that legacy migration. Field KP40A observations were of the existing DKMS 1.0 driver, not this candidate.

## Critical generic-AUR regression gate

The source map and BUILD_EXCLUSIVE permit only three exact CachyOS releases. Official Arch/linux-zen and future releases receive no patched module. On an upgrade, an old DKMS module may be removed by the pre-transaction path while the new package's post-hook excludes that kernel. Stock restoration is conditional on intact DKMS backup/active-state metadata; even a successful stock fallback does not preserve the Beitong workaround. This is a code-path assessment, not a completed official-Arch migration test.

The old public recipe can package an uncompressed host-kernel `xpad.ko` while DKMS also manages compressed/generated files. The new source-only payload avoids adding another such file, but its candidate-only clean-root success does not establish conflict-free removal/migration of all old package-owned and DKMS-generated files. Do not use `--overwrite`, force installation, widen the regex or fall back to older driver source to hide this gap.

Official Arch public metadata currently names these missing test packages:

- `linux 7.3.4.arch1-2` (core, x86_64)
- `linux-zen 7.3.4.zen2-2` (extra, x86_64)

Their actual header release strings, compiler configuration and exact patched source must be verified, not inferred from package names. No matching official Arch headers were available locally and no target was guessed/enabled. Existing CachyOS LTS GCC builds are only CachyOS evidence.

**Primary remaining release blocker:** preservation of the generic AUR package's supported-user upgrade behavior, especially official Arch/linux-zen and the legacy 1.0 migration. Close it by obtaining verified official headers/sources, reviewing the source deltas, testing the exact targets and real old-package migration in the controlled root without executing unreviewed scripts. Alternatively keep this as a clearly separate CachyOS prerelease; do not silently replace the existing generic package. A separate package identity would also need conflict/ownership review before creation.

Authenticated AUR write authority, production signing/boot integration and candidate hardware input/reconnect remain explicitly unverified prerequisites; none is implied green by these local tests. No push, AUR package creation, GitHub mutation, host driver installation/reload or publication occurred.

## Local artifacts

- `xpad-beitong-dkms-1.3-1-any.pkg.tar.zst`: SHA-256 `e74031c4484f61baa53d8790d626d082ef1c970c11d8244fd7ba653802f87357`
- `xpad-beitong-dkms-1.3-1.src.tar.gz`: SHA-256 `5ef132baa89c5478b45450d8b5f7162b6c780bb00fdc3060c0146d9e4522eef9`

Full package/source manifests and `audit-final.json` are in the evidence root. Real transaction logs, UID maps, fixture policies, restoration hashes and the zero-call loader log are in `lifecycle/evidence/`. The source/version fixtures are test artifacts only and are not publication payloads.
