# Release suitability review — 2026-11-14

The former Linux-v6.18 candidate `9e626f4` is **red for release** despite successful compilation. Its missing stock changes were confirmed by full source diffs, not speculation. The replacement local candidate fixes source selection for exactly three reviewed CachyOS releases; it is not a universal Arch/Mint driver package or a hardware-validated release.

## Stock comparison

The installed headers omit `xpad.c`. Exact official stable snapshots and corresponding CachyOS source tags were independently fetched as text; all three pairs have identical Git blobs. See [SOURCES.md](SOURCES.md) for immutable commits, hashes, tag mapping and the remaining installed-binary provenance limit.

Relative to Linux v6.18, all three snapshots retain the following changes:

- A Share-button packet-length guard, `if (len >= offset)`, before `data[len - offset]`; the old candidate could lose that bounds check.
- PDP Marvel `0e6f:0147` classified as Xbox 360 rather than Xbox One.
- 23 additional device IDs in the initial two snapshots (24 in 7.3.4), including CRKD, ASUS RAIKIRI II, Razer Wolverine V3, Azeron, Corsair and others, plus matching vendor entries.
- Existing `20bc:5134`/`514a` entries and Xbox 360 vendor interface matching for `20bc`.

7.3.3 additionally has RedOctane `3958` vendor matching, allocation API conversions and comment cleanup compared with 6.18.60. The new strategy retains each target's own changes rather than assuming one newer source is interchangeable across kernels.

Neither stock snapshot contains the project's Beitong `FLAG_FORCE_INIT`/`btp_*` sequence, the fork's `FLAG_READ_XUSB10`/Microsoft feature-descriptor request, or a `20dd:518b` HID handler. Generic Xbox One GIP support and the preexisting Xbox 360 magic request are present; these are not the missing Beitong-specific quirks. No `518b` device entry exists in either stock snapshot. This proves absence in these exact sources, not that a specific untested controller needs a particular quirk.

Local complete diffs and read-only recipes are in `/home/robin/Documents/Codex/2026-11-14/task/xpad-validation/stock-review/`. Snapshot bytes in this checkout match those reviewed files.

## Gates

| Gate | State | Evidence / remaining work |
|---|---|---|
| Preserve original local candidate | Green | `9e626f4` remains ancestor and tip of `local/source-only-dkms`; review continues separately. |
| Preserve stock source for allowed releases | Green, scoped | Exact stock snapshot per target; no old-source fallback; source and patch hashes in PKGBUILD. Generic recipe provenance does not reconstruct installed znver4 binaries. |
| Unknown/new kernel safety | Green | DKMS allowlist now returns 77 for unreviewed 7.3.5; 7.3.4 is independently reviewed and added; wrapper rejects unknown KVER and mismatched headers. New releases require review. |
| Source-only package and repeatability | Green | Nine checksum inputs pass; repeat prepare yields identical source hashes; checksum tampering rejected; archive contains only six source/config payload files. |
| Actual compile and DKMS build | Green, scoped | Current 7.3.4 and LTS headers compile; old 7.3.3 header is absent and only its prior evidence is retained; isolated DKMS status `built`, matching vermagic. Unsigned test outputs never installed. |
| Current driver/hardware regression test | Red / not performed | No device interaction. Validate intended original-device fix, unrelated-controller behavior, reconnect and D-pad semantics in a separately authorized session. |
| Installation/removal, signing and activation | Red / not performed | Only isolated add/build/status tested. Transaction lifecycle and signature acceptance need a controlled test before release. |
| Other kernels / official Arch / Mint | Red / unsupported | Intentionally excluded. Do not market as general compatibility. |
| KP70C1 Mint support | Red / unverified | No device change included. Follow [reporter plan](KP70C1-VALIDATION.md); ID-only change was already reported ineffective. |
| Publication / GitHub changes | Not requested / not done | No push, merge, comment, release or AUR update. |

The clear packaging improvement has been implemented and tested locally, but green build gates do not close hardware or activation gates. Keep publication blocked. If target kernels advance before a release, re-review their exact stock source and extend the matrix rather than weakening the safeguards.

## Current extension

See [VALIDATION-7.3.4.md](VALIDATION-7.3.4.md): 7.3.4 exact sources have been checked, the one-row stock device addition is preserved, and 7.3.4/LTS isolated DKMS builds pass. The compiler patch-version warning remains documented. No installation or hardware gate is closed by this build. Field observations of the running DKMS 1.0 driver are not candidate 1.3 validation.
