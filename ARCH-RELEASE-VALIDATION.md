# Official Arch and legacy migration validation — 2026-11-15

Worktree: `/home/robin/Documents/Codex/2026-11-14/task/xpad-arch`
Branch: `local/arch-release-validation`
Base preserved: `4737dd9923642d1465bc8e5d8b22c04b20254c31`
Candidate version: **1.4-1**, unpublished.
Evidence root: `/home/robin/Documents/Codex/2026-11-14/task/xpad-validation/arch-release`.

## Authenticated inputs and exact targets

Official current packages remain the requested versions: linux/linux-headers `7.3.4.arch1-2` and linux-zen/linux-zen-headers `7.3.4.zen2-2`. All four kernel/header archives were downloaded over ordinary validated HTTPS and their detached signatures were verified **before extraction/use**, against the installed trusted Arch keyring. No signature, TLS check or SSH host-key check was bypassed. No new verification key, account credential or SSH key was generated/downloaded; the installed public keyring was decoded into workspace-only verification data.

Both packages and both raw source-tag signatures validate to the known Arch packager fingerprint `83BC8889351B5DEBBB68416EB8AC08600F108CDF`. The signed `.BUILDINFO` records authenticate the exact official PKGBUILD hashes. Full signature statuses, recipe hashes, verified source commits and file Git object IDs are in SOURCES.md and the evidence root. The signed source Git tree chains give the same xpad blob `d2eb48d98fead7d89eb3e45613a52176c4fa5fad` already pinned for 7.3.4. No distro-specific xpad delta or unreviewed source substitution is involved.

| Target release read from authenticated headers | Compiler config | Test result |
|---|---|---|
| `7.3.4-arch1-2` | GCC 16.2.1 / BFD / no LTO | Actual build/install/upgrade/remove and legacy migration pass |
| `7.3.4-zen2-2-zen` | GCC 16.2.1 / BFD / no LTO | Actual build/install/upgrade/remove and legacy migration pass |
| `7.3.4-1-cachyos` | Clang / LLD / ThinLTO | Actual regression transactions pass; existing Clang 23.1.5 vs kernel 23.1.4 warning retained |
| `6.18.60-2-cachyos-lts` | GCC 16.2.1 / BFD / no LTO | Actual regression transactions pass |
| `7.3.3-1-cachyos` | Previously reviewed Clang target | Mapping/source retained byte-unchanged; headers absent, not freshly rebuilt |

Only the two exact authenticated Arch release aliases are added. They share the proven 7.3.4 source/patch rather than duplicating or downgrading it. Existing CachyOS source/patch files remain unchanged. All five mappings are covered by offline tests; unknown targets still fail. An actual isolated `dkms build` request for the synthetic negative case `unsupported-test-kernel` returned **77 before compilation**.

## Actual package and legacy transactions

These are real pacman/DKMS transactions in a controlled alternate root, not a hook model or a claim that an Arch kernel was booted. Kernel/header data were seeded from the verified archives; trusted already-installed tools and dependency metadata were used. Host kernels/drivers were not installed, removed or loaded.

The observed transactions were:

1. Install candidate `1.4-1`; all four available targets reach DKMS `installed` with exact matching vermagic.
2. Upgrade to self-authored, metadata-only pkgrel fixture `1.4-2`; actual pre/post DKMS hooks run, rebuild and reinstall all four targets.
3. Remove candidate; all registrations and candidate source paths disappear, and all four stock module files are restored byte-for-byte.
4. Install the existing historical `1.0-1` package archive. Its `.INSTALL` bytes and declared Makefile/patch/config match public AUR commit `e3e25ce5d8063226a08580427fc1331f80284167`; `.INSTALL` SHA-256 is `1a8358c0cc36a8dce9a2d0bfb451db5cb4ed74d3c38fa937852a5dc974ad5d7a`. The legacy source SHA matches the known installed historical source. The old PKGBUILD itself is **not executed**.
5. Upgrade that old package to candidate `1.4-1`; real hooks remove old DKMS 1.0, pacman removes its old package-owned precompiled RC-kernel `.ko`, and new DKMS 1.4 installs on all four targets. Old `/usr/src/xpad-beitong-1.0`, DKMS 1.0 state and old owned `.ko` paths are verified absent.
6. Remove migrated candidate; stock modules again restore exactly and all candidate registrations disappear.

AUR distributes recipes, not a universal binary: the legacy input is the preexisting local 1.0-1 archive with exactly matching public script/layout. Its original recipe selected source dynamically, so this is a concrete historical migration case, not every possible legacy user build. The legacy baseline only obtained a working Clang/CachyOS DKMS installation; its forced LLVM behavior did not establish GCC-target operation. New candidate installation succeeds for both official GCC targets.

The reviewed old script attempted `modprobe xpad` once. The logging stub intercepted it and returned failure; the old script suppresses that failure and prints a success message, which is **not** hardware evidence. No rmmod/insmod/systemctl/signing command reached a real host action. Candidate installation/upgrades/removals added **zero** loader calls. No contributor PR recipe ran.

## Isolation and signing boundaries

Bubblewrap uses independent user/mount/PID/network namespaces. Namespace UID/GID 0 maps only to host UID/GID 1000; CAP_SYS_MODULE is dropped. Host `/usr` and all target headers are read-only. Writable package DB, sources, modules, DKMS state and logs are workspace fixtures. No host `/etc`, `/var`, `/home`, `/sys` or input devices are exposed; the network namespace contains only loopback. PATH stubs intercept reviewed legacy loader/service/signing commands, and kernel namespace/capability checks remain a second barrier.

Only standard Arch's three DKMS transaction hooks are exposed. The fixture retains normal optional signature policy for unsigned local AUR/test packages; official distro packages were independently signature-verified before use. Its own DKMS config sets `try_sign_modules=false`, avoiding any access to host signing private keys or policy. A fixture-only `DisableSandboxNetwork` avoids nested pacman sandbox failure while the outer network namespace remains enforced. No host security/signing/network/permission setting was changed and no sudo was used.

The new package does **not** disable signing: it inherits the installed DKMS framework's policy and has no signing bypass. Verified official headers enable module signatures and do not force them at build config level; runtime policy can still enforce signatures. Production key enrollment, Secure Boot acceptance and actual kernel loading were not tested and must not be inferred from this unsigned isolated test. Host-specific initramfs/boot hooks and physical controller input/reconnect also remain untested for this candidate.

## Fingerprints: installed candidate files, not live host modules

Full rows are in `lifecycle/evidence/legacy-to-candidate-modules.json`; each target's candidate build ID differs from its authenticated/restored stock file. Exact stock SHA-256 restoration is asserted after both removal paths.

| Target | Candidate srcversion | Candidate build ID |
|---|---|---|
| Arch linux | `01E6177868900E25C41CFFB` | `c6ce4c4d664cc20ea00c9cfb2fa6e82971a3c5ef` |
| Arch linux-zen | `01E6177868900E25C41CFFB` | `2275f60a67cda5b8ee881f8724ffaa2b16dc4a03` |
| CachyOS 7.3.4 | `01E6177868900E25C41CFFB` | `abac5c005e4b8f248eb36577964dd8e63fb859ca` |
| CachyOS LTS | `21F7D0CBC5A900E2D7C0DF9` | `39595d4a216187fa99b9915113c215440f8a61ab` |

All observed vermagic strings begin with the exact corresponding target release and end `SMP preempt mod_unload`. Files were inspected with modinfo and GNU build-ID data; no candidate was loaded into the host kernel.

## AUR authentication and publication plan — not executed

The verified public target remains `https://aur.archlinux.org/xpad-beitong-dkms.git`, current known public `master`/HEAD `e3e25ce5d8063226a08580427fc1331f80284167`, public version 1.0-1 and maintainer Robin6750. Candidate 1.4-1 compares newer than both public 1.0-1 and the preserved local 1.0-2 edit.

A read-only check found an existing AUR known_hosts entry, but **no explicit AUR Host/HostName/IdentityFile configuration**. No private/public SSH key contents were printed, no key or credential was created, and no authentication was attempted with guessed/default identities. Account write control remains unverified.

The next separate action requiring an identified existing identity is a **read-only AUR account preflight**: confirm which already-authorized SSH identity belongs to Robin6750, then run BatchMode with StrictHostKeyChecking=yes, UpdateHostKeys=no and no forwarding, requesting only AUR `help`. Do not add host keys, bypass a mismatch or try unrelated identities. A successful username response must match the package maintainer before publication.

After that, the parent can decide publication under the user's authorization, in a fresh AUR checkout rather than the dirty cache:

1. Re-read AUR RPC and remote HEAD; abort/review if the expected version/commit or ownership has changed.
2. Stage only reviewed PKGBUILD, generated .SRCINFO, every checksummed source input and appropriate documentation; exclude binaries, test fixtures, verification keyrings, downloads and credentials. Verify source archive, hashes, license/attribution and monotonic version again.
3. Review the exact AUR commit diff and perform one ordinary, non-force push to the authorized existing package. No new package/account is needed.
4. Read back anonymous `git ls-remote` plus the actual remote commit/files and AUR RPC. Acceptance requires the pushed commit and published package version both match candidate 1.4-1; a push exit code alone is insufficient. Until those read-backs succeed, do not claim publication.

This round performs **no push/merge/comment/package creation**. Raw PR #3 and #4 remain unsafe as-is: #3 still forces LLVM in DKMS, while #4 retains host-dependent unchecked network acquisition and failure/repeat issues. The independent successor retains `ilevnn`'s bug-report attribution and Zixing Liu's patch attribution; no repeated thanks were posted.

## Release scope

The current official Arch/linux-zen GCC gap and the tested legacy migration gap are now closed for the listed exact targets/case. This is not universal rolling-kernel support: unreviewed releases are intentionally refused, and stock fallback is not the Beitong workaround. Users needing an unlisted kernel should not upgrade this bounded package expecting the patch to remain available; that exact release must be reviewed and added first. No support is guessed for KP70C1 or other untested hardware.

Evidence includes signature logs, authenticated PKGBUILD/source objects, real transaction/helper/compiler logs, namespace maps, intercepted calls, old-file cleanup and module fingerprints. Production signing/boot integration, candidate hardware input and AUR authenticated publication are still explicit boundaries, not silently green gates.
