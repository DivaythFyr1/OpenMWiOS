# Phase 1 — Repository recovery and audit

Audit date: 2026-10-24. Scope: Phase 1 of [ROADMAP.md](ROADMAP.md) only.

## Cloud recovery update — 2026-10-25

The original local audit below is retained as historical evidence. Live Git access now works for both repositories through platform authentication. All 29 upstream branch tips and three tags match the audit. All 22 advertised PR heads and merge refs have been fetched, including external #21 and new #22. See the completed [live inventory](branch-inventory.md#live-cloud-refresh--2026-10-25).

WO33 `49f5f0bd80e83ef87eaebd3f69c07072796738aa` remains the recommended baseline: its product tree is identical to `93f892dd0cf9834259b4cad2045ddb2ef9c53ed9` outside Evidence, and the newly discovered PR adds only deferred workflows. Original main is an ancestor. A review branch now merges the fork's audit-document commit `3e86accde6b3bc01b9f6475ad85dbed746db21bc` into WO33 without rewriting either history. No renderer, lifecycle, dependency-pin, test, or feature changes were introduced.

API requests via `gh api`, including an escalated attempt, failed with Forbidden. A direct HTTPS diagnostic identified proxy CONNECT HTTP 403 before an API response. This is not evidence of an invalid token or absent repository write permission. API fork relationship, authenticated identity, paginated PR states/reviews/checks remain unverified. Git push dry-run succeeded; actual publication outcome is recorded in [consolidation status](consolidation-status.md). The missing `api.github.com` network destination is saved for environment review, not assumed active.

Current Linux validation: the repository bootstrap fetched all five exact dependency pins and successfully applied all 15 OpenMW and nine GL4ES patches. Python 3.12.14, GCC, and CMake 4.3.4 ran all **148 host tests successfully, with no skips**. This is a fresh cloud result, separate from the earlier Mac results below. The full macOS source-validation wrapper, Xcode generation/build, signing, iPhone launch, and device behavior were not validated here. Optional WO38 GLib and local ICU adaptations were not adopted without their required Mac reproduction.

A complete verified Git bundle of recovered project refs was saved outside the checkout at `/workspace/openmw-recovery-2026-10-25.bundle` (SHA-256 `8f80213c2f015c691b8d3fc02405ccf87be423dfded88d5e7039e64405049aeb`). It preserves unmerged branches and PR objects, including synthetic merge refs; it is a local recovery artifact, not a published backup. The destination already advertises all audited upstream branches and tags. No upstream branch was changed or deleted.

## Executive finding (original audit)

**Recommend `codex/wo33-blend-state-transition` at `49f5f0bd80e83ef87eaebd3f69c07072796738aa` as the consolidation starting point.** Its application, dependency, patch, and test contents are identical to the device-qualified correction commit `93f892dd0cf9834259b4cad2045ddb2ef9c53ed9`; the extra commit preserves the final qualification evidence. This is the strongest documented functional baseline, not a claim that all renderer or lifecycle problems are solved.

The most developed published candidate is WO38 at `7dbedda156b9ab2de1b23f7119f58a6f6a0d6667`, corresponding to release `ios-fast-67`. Its additional diagnostics and Pause correction have build/host-test evidence but no recorded final device qualification. Preserve it as a recovery/reference point rather than promoting its entire tree to production.

Upstream `main` contains only a README. Development is distributed across a largely cumulative implementation history, an independently advancing documentation/decision branch, and several experimental branches. GitHub's observed PR index lists 21 open PRs and zero closed PRs; that does **not** mean their changes are absent from later branches. WO30, for example, was already integrated by an ordinary Git merge.

The working IPA has a strong published provenance candidate, but the particular IPA installed on the user's iPhone has not been identified by checksum. Xcode compilation and runtime compatibility must remain separate: an existing local Debug executable was built with iOS SDK 27.1, whereas the published Fast workflow selects Xcode 16.4. The audited SDL2 integration uses the legacy UIKit application lifecycle.

## Scope, evidence levels, and limitations

The requested workspace initially contained only the roadmap and was not a Git repository. A pre-existing checkout at `/Users/jan-henrikniestroj/dev/OpenMWiOS` supplied:

- 29 remote-tracking branch heads, three tags, and 203 reachable commits; it is not a shallow checkout.
- Pinned dependency checkouts, generated Xcode projects, installed dependency metadata, and an existing Debug app/dSYM.
- Upstream execution reports, device-result records, and later acceptance/rejection reviews.

The checkout was inspected read-only. Its existing modification to `triplets/arm64-ios-openmw-release.cmake` and untracked `.before-icu-fix` backup were preserved. Committed source was exported into temporary directories for validation; no application changes, branch merges/deletions, builds, installs, workflow dispatches, or implementation work were performed.

Evidence labels used here:

| Label | Meaning |
|---|---|
| Verified locally | Directly observed Git object, source, metadata, or audit command result |
| Verified public metadata | Observed GitHub page, release description, workflow source, or run status; some pages are cached |
| Upstream-reported device evidence | Committed report with artifact/capture identities; not a device test performed by this audit |
| Hypothesis | Plausible interpretation requiring further evidence |

**Recovery limitations:** direct GitHub Git/API access failed DNS resolution, and the saved `gh` authentication check reported invalid credentials. Public web access worked partially. Consequently, this audit did not create the roadmap's requested public fork, refresh remote refs, download and hash the release IPA, or obtain a fresh exhaustive API inventory of PR reviews/checks and workflow runs. Several older PR conversation pages were inaccessible; their indexed titles and available implementation histories were inspected instead. The 29-head inventory is exhaustive for the local snapshot, not certified exhaustive for the live remote on October 24. The local packed-ref file is dated October 19; that timestamp is not proof of a successful fetch on that date.

The documents are ready for review, with the remote-refresh/fork requirement explicitly outstanding. The recommendation can be assessed now; adoption must first compare a fresh remote inventory against [branch-inventory.md](branch-inventory.md). No absence of inaccessible remote evidence is treated as proof that it does not exist.

### Access recovery verification — 2026-10-25

The existing local credential file was located and read only into process memory for HTTPS requests to GitHub's `/user` and `/repos/arjunyerevan95-dot/OpenMWiOS` API endpoints. Its contents were not printed, logged, copied into documentation, placed in command arguments or remote URLs, or modified. Both requests failed DNS resolution for `api.github.com` before any HTTP response. **Token validity, authenticated identity, and repository permissions remain unverified.** The earlier saved `gh` account check is not evidence that this separately supplied token is invalid.

A public Git fetch was also attempted in the isolated empty repository `/private/tmp/openmw-access-recovery-c634mtfj`, requesting all upstream heads, tags, PR heads, and available PR merge refs. No credentials were needed for this public read. It failed with exit code 128 because `github.com` could not be resolved; no refs were fetched. The existing working checkout was not changed.

A follow-up explicitly tested `gh api` against both API endpoints using the supplied credential through the child process's `GH_TOKEN` environment variable, without saving a login or exposing the credential in arguments or output. Both calls exited with code 1 and reported a connection failure. Neither reported HTTP 401, 403, or 404. This independently confirms that using `gh` did not restore connectivity; it does not establish token validity or permissions.

Local revalidation found all 29 cached branch heads and all three tags unchanged from the inventory, with 203 reachable commits. WO33 still points to `49f5f0bd80e83ef87eaebd3f69c07072796738aa`; its direct parent is `93f892dd0cf9834259b4cad2045ddb2ef9c53ed9`, and all six changed files are under `Evidence/WO-033/`. The baseline recommendation therefore remains supported by the cached evidence, but has not been revalidated against the live upstream. The fresh inventory, external PR #21's full head SHA, authentication, and permissions remain outstanding. Phase 2 has not started because the requested access and refresh prerequisites could not be completed.

## Baseline assessment

| State | Evidence and assessment |
|---|---|
| `main` — `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` | One README; no buildable port. Reject as a source baseline. |
| WO29 correction — `45c1d8c696fb328d977893b79efc78689a3f4d08` | Upstream reports corrected non-ARC icon ownership, successful launch, indoor play, and exterior traversal. Useful fallback, but predates later touch customization and accepted blend correction. |
| WO30 source — `195f3a4bbcfd17ecd46546f3e28d3ee8558bed27` | Touch customization and earlier renderer investigation; older accepted product point. Not the most complete qualified renderer state. |
| WO33 correction — `93f892dd0cf9834259b4cad2045ddb2ef9c53ed9` | Narrow OSG/GL4ES blend-cache correction, successful Fast build, artifact identities, before/after runtime trace, and recorded physical-device improvements. Strongest qualified engineering state. |
| WO33 evidence head — `49f5f0bd80e83ef87eaebd3f69c07072796738aa` | Same product as `93f892d`, plus six final evidence documents. Recommended exact starting commit. |
| WO38 release/evidence head — `7dbedda156b9ab2de1b23f7119f58a6f6a0d6667` | Contains WO33 correction, cold-OSG build recovery, later observer, and Pause candidate. Latest published build candidate; physical Pause and target-attribution qualification remain unrecorded. |
| WO29 branch head — `6001b1f39dcfb94f594d3d1a80d2b801749c8a26` | Latest recorded decision/coordination state, through WO39. Product source diverged at WO30; do not mistake the newest administrative commit for the newest implementation. |

Verified comparisons:

- `93f892d..49f5f0b` changes only `Evidence/WO-033/`.
- WO38 and WO33 evidence head share `93f892d` as their merge base. WO38 does not contain `49f5f0b`, so its WO33 report still describes an earlier failure despite containing the accepted correction.
- WO29's decision branch and the implementation line share merge commit `dfe9e1e875c7020658aa59d22121a7cc0061ac69`. Its subsequent 30 commits change only documentation, work orders, decisions, and evidence.
- The WO34 terrain patch is absent from WO38. WO35/36 are evidence-only branches off `93f892d`.

Sources: immutable [WO33 device record](https://github.com/arjunyerevan95-dot/OpenMWiOS/blob/49f5f0bd80e83ef87eaebd3f69c07072796738aa/Evidence/WO-033/device-capture.md), [WO33 final review](https://github.com/arjunyerevan95-dot/OpenMWiOS/blob/6001b1f39dcfb94f594d3d1a80d2b801749c8a26/Evidence/WO-033/orchestrator-final-review.md), and [WO38 final review](https://github.com/arjunyerevan95-dot/OpenMWiOS/blob/6001b1f39dcfb94f594d3d1a80d2b801749c8a26/Evidence/WO-038/orchestrator-final-review.md). Their contents were read from local Git objects, not inferred from their titles.

## IPA provenance

### Published candidate: Development Build 67

The [release description](https://github.com/arjunyerevan95-dot/OpenMWiOS/releases/tag/ios-fast-67), [successful run](https://github.com/arjunyerevan95-dot/OpenMWiOS/actions/runs/33306995685), and committed WO38 evidence agree on:

| Identity | Value |
|---|---|
| Build source | `457ab881442302a9bd59435c1878ed4e72f6e52b` |
| Branch | `codex/wo38-cold-osg-attribution` |
| Release tag target | `7dbedda156b9ab2de1b23f7119f58a6f6a0d6667` |
| Fast run / number | `33306995685` / 67 |
| Original Actions artifact | `OpenMW-iOS-fast-67`, ID `9730898326` |
| IPA SHA-256 | `9312ea3b1ad757e9cee8a22785907f93ad9c68a33e02d845210ff5f733660593` |
| Executable SHA-256, reported | `26a73e55775a15bfdb60cc6c05861e1f790f60dfc920a5ef7b4087f7822ed912` |
| IPA size, upstream final review | 39,159,562 bytes |
| Original artifact-wrapper digest | `41709748e6cad3d8e48b1244ae42ee96a35ea7eb2607b751f8d6f834b69c315b` |
| Packaging | Unsigned arm64 iPhone IPA; minimum iOS 16.3; no game data |

The tag points to an evidence-only successor of the source commit: `git diff 457ab88 7dbedda` changes three WO38 Markdown files, not product code. Reproducing the tag therefore selects the same product source, but provenance should continue to name the actual run SHA.

Upstream's September 19 review reports that the original seven-day Actions artifact expired on September 6 and that a surviving local IPA on the upstream maintainer's Windows machine was hash-verified. The release page provides a separate publication record; expiration of the Actions artifact does not establish expiration of the release asset. Neither the Windows file nor the release binary was available for independent binary inspection in this audit.

**Hypothesis:** if the user's IPA came from the public Development Build 67 release, its source is `457ab88`. This is not yet a verified identity for the user's installed app. Re-signing can change the IPA and executable hashes; compare the original downloaded file first, then Mach-O UUID/build metadata and packaged resources when investigating a re-signed copy. A wrapper ZIP digest is not an IPA digest.

### Device-qualified reference: Fast 55 / WO33

| Identity | Value |
|---|---|
| Source | `93f892dd0cf9834259b4cad2045ddb2ef9c53ed9` |
| Run | [32771773194](https://github.com/arjunyerevan95-dot/OpenMWiOS/actions/runs/32771773194) |
| Artifact | `OpenMW-iOS-fast-55`, ID `9538962155` |
| IPA SHA-256 | `34eb8106c60138f30da8b59083ca026fda013f68870ddc658c1584b6e939ac4e` |
| Executable SHA-256 | `c759b9d09df6a2cffe7657839bd3db25999a399743e811a7846a406a5826874c` |
| Mach-O UUID | `FD8BB9B2-AF3F-3CFD-ACAE-B20D1E5D0664` |

The worker report originally omitted the UUID; the final acceptance review records an independent extraction. Preserve both records rather than silently rewriting the historical omission.

The other observed releases, `delivery-run-59-artifacts` and `recovery-evidence-milestone2b-0053c502`, preserve early delivery/recovery evidence. In particular, the latter explicitly reports a failed Gate 4 link and no complete IPA/runtime result. They are not substitutes for the later working game build.

### Existing local build

Read-only inspection found `build/ios/Debug/openmw.app/openmw` and a corresponding dSYM in the adjacent checkout:

- Mach-O UUID: `82D147E3-2C89-3C29-8D00-2EFD50A2A805`, arm64.
- `LC_BUILD_VERSION`: platform IOS, minimum 16.3, SDK 27.1.
- Built Info.plist: Xcode 27.1 / build `27A9275`, iPhoneOS 27.1, a local custom bundle identifier, no `UIApplicationSceneManifest`.

This corroborates the existence of a local Xcode 27 build. It does not establish a clean reproducible build, precise source-to-binary identity, or successful launch. No IPA was found in the searched Downloads/development locations, and no new crash capture was performed.

## Renderer PRs #17–#20

These PRs are sequential investigations with later amendments; their initial descriptions alone are insufficient. Their production code is already cumulative in WO33.

| PR | Actual progression | Disposition |
|---|---|---|
| [#17 / WO31](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/17) | `50aa047` introduced bounded app-owned JSONL and engine/GL4ES probes. It crashed from non-ARC diagnostic-string lifetime errors. `8140aa4` repaired ownership; `626b332` moved probes to active paths. Final evidence `123ae04` shows functioning transport but budgets exhausted before representative draws/fog consumption. | Keep inherited lifetime/probe prerequisites. Do not label this a renderer fix or complete causal evidence. |
| [#18 / WO32](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/18) | `4b626d8` targeted draws and fog generations; `79231c0` repaired fixture context. `1625713` routed OSG blend operations through GL4ES. `c9161e5` only extended the build timeout. Successful run `32649331052` still produced four smoke draws with blending disabled. | Routing change alone was falsified as sufficient; retain it as inherited context for WO33 rather than cherry-picking it as a standalone proven cure. |
| [#19 / WO33](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/19) | `f0427d8` traced transitions. `10b8888` repaired GL4ES patch materialization; `fd300ba` repaired OSG patch representation. A subsequent device trace exposed OSG suppressing an enable call while GL4ES tracked blending off. `93f892d` reasserted cache-matching `GL_BLEND` through GL4ES on the Apple/manual-init route. | Accepted targeted correction; preserve its prerequisites and qualification evidence `49f5f0b`. |
| [#20 / WO34](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/20) | `398a917` expanded terrain coverage to the far-frustum corner. Build and installation passed. Evidence `c82542b` records no material improvement to white gaps, blue horizon, or distant black silhouettes. | Preserve as rejected causal experiment. Do not include its terrain patch in the baseline. |

WO33's recorded corrected trace has 55 OSG reassertions, 55 GL4ES enable ingress records, and four targeted smoke draws with `blend=1`, versus four with `blend=0` before correction. Upstream reports improved smoke, spell effects, and foliage transparency with eight screenshots. The smoke mechanism is supported by a targeted trace; improvement in sampled foliage is a collateral device observation, not proof that every vegetation/texture defect shares that cause. The roadmap's current foliage symptoms remain valid observations requiring new qualification against the selected source and settings.

Important diagnostic limitations remain:

- PR review comments identify stale texture-name classification, inactive texture units being mistaken for active smoke targets, finite sample-budget exhaustion, and incomplete direct-array trace flushing. These are evidence-quality concerns, not established explanations for the user's current visual defects. This audit does not declare every review item resolved.
- **Verified documentation contradiction:** `ios/openmw_ios_bootstrap.mm:122` at both recommended and release snapshots calls `setenv("OPENMW_IOS_RENDERER_DIAGNOSTICS", "1", 1)`. The recorder's environment check therefore does not make ordinary bootstrap launches opt-in, contrary to the WO33 review. A 256 KiB file cap limits output volume, not necessarily all per-draw work. Performance qualification must account for this.
- WO37/38's observer uses projected bounding boxes, a 96-candidate limit, center-RGBA samples, and one-shot presentation completion. It explicitly lacks raw GLES2 depth sampling and observed sky-RTT output. Equal pixels do not prove absent geometry; a sampled intermediate draw does not establish ownership of the final displayed pixel.
- WO35/36 configuration experiments did not eliminate the horizon/silhouette failures. Their source branches contain evidence only. WO36 reports testing the installed WO34 binary; that device experiment must not be misattributed to an unmodified `93f892d` binary merely because its evidence branch starts there.

## Dependency and build architecture

The repository is a platform bridge and ordered patch stack over pinned OpenMW, not a vendored replacement engine. `scripts/bootstrap.sh` fetches pinned dependencies, applies numbered OpenMW/GL4ES patches, and copies `ios/` into the generated engine checkout. `scripts/build-ios.sh` installs vcpkg packages, builds static LuaJIT and GL4ES, and generates `build/ios/OpenMW.xcodeproj` with CMake's Xcode generator. It does not itself compile the final `openmw` app.

| Component | Pinned revision/version | Source |
|---|---|---|
| OpenMW | `f4bec41444214a7903bebd178389ca22ca13f646` / reported 0.51.0 | `versions.env` |
| OpenMW OSG fork | `01cc2b585c8456a4ff843066b7e1a8715558289f` / 3.6.5 | `versions.env`, engine FetchContent |
| GL4ES | `c9895df34cd466c23bc60c2bd3db3d87e98fcbe7` / 1.1.6 | `versions.env` |
| ios-cmake | `99f99df73dc752c7e88916fc1f9df6b9f8c40f8d` | `versions.env` |
| vcpkg | `cd61e1e26a038e82d6550a3ebbe0fbbfe7da78e3` | `versions.env` |
| LuaJIT | `8e6520a7aecd0517e792b359afbbfd7274791f5f` | `versions.env`, separate host/target build |
| SDL2 | 2.32.10, port revision 1 | Pinned vcpkg port and local installed package |
| Bullet | 3.17 | OpenMW `extern/CMakeLists.txt`, archive SHA-512 |
| MyGUI | 3.4.3 | OpenMW `extern/CMakeLists.txt`, archive SHA-512 |
| RecastNavigation | `03259f3287ff8330f0d66fcd98d022edddffaa97` | OpenMW FetchContent, archive SHA-512 |
| SQLite | 3.41.1 / amalgamation 3410100 | OpenMW FetchContent, archive SHA-512 |
| Build tools | CMake 4.3.4; ShellCheck 0.11.0 | Checksum-pinned installers and `versions.env` |

The vcpkg manifest also requires Boost.Geometry/Iostreams/ProgramOptions 1.91.0, FFmpeg 8.1.2, FreeType 2.14.3, ICU 78.3#1, libjpeg-turbo 3.1.4.1, libpng 1.6.58, LZ4 1.10.0, OpenAL Soft 1.25.1#2, yaml-cpp 0.9.0#1, and zlib 1.3.2#1 at the inspected vcpkg pin. FFmpeg enables avcodec/avformat/swresample/swscale without default features; FreeType also disables default features. Preserve transitive package resolution with the vcpkg commit, not this abbreviated direct-dependency list alone.

Local dependency Git HEADs match the five fetched revisions in `versions.env`. Recommended and release snapshots have identical `versions.env`, `vcpkg.json`, and committed triplet contents. The local package status file corroborates the SDL and direct-package versions; it is not proof that every existing archive is clean or reproducible.

Build constraints:

- Device-only arm64 / `PLATFORM=OS64`; deployment target 16.3; GL4ES exports desktop GL over GLES2 (`DEFAULT_ES=2`, `LIBGL_ES=2`, manual initialization, no automatic loader/constructor).
- Static native dependencies and OSG plugin registrars must be retained. Existing archive/link-manifest and registrar checks are valuable recovery assets.
- `ENABLE_ARC=OFF` applies to the OpenMW/OSG graph. Objective-C++ ownership requires explicit care; both icon and diagnostic crashes demonstrate this.
- The `arm64-ios-openmw-release` triplet fixes `VCPKG_BUILD_TYPE=release`. Selecting app Debug does not produce Debug variants of all third-party libraries.
- LuaJIT builds host utilities with the macOS SDK and its target archive with the iPhoneOS SDK. Avoid treating a same-architecture host library as an iOS library.
- The committed ShellCheck installer pins a Darwin x86_64 binary. Native Apple Silicon tooling/Rosetta availability needs an explicit documented choice rather than an assumption.

Sources: [versions](https://github.com/arjunyerevan95-dot/OpenMWiOS/blob/49f5f0bd80e83ef87eaebd3f69c07072796738aa/versions.env), [build script](https://github.com/arjunyerevan95-dot/OpenMWiOS/blob/49f5f0bd80e83ef87eaebd3f69c07072796738aa/scripts/build-ios.sh), [platform targets](https://github.com/arjunyerevan95-dot/OpenMWiOS/blob/49f5f0bd80e83ef87eaebd3f69c07072796738aa/ios/CMakeLists.txt), and [pinned engine dependencies](https://github.com/OpenMW/openmw/blob/f4bec41444214a7903bebd178389ca22ca13f646/extern/CMakeLists.txt); inspected locally where web retrieval was unavailable.

## Existing workflows and reproducibility risks

| Workflow | Actual behavior | Audit disposition |
|---|---|---|
| `.github/workflows/ios-fast.yml` | PR/manual triggers, Release, Intel macOS runner, Xcode 16.4, three-hour timeout, cached source/packages/build state, unsigned production app verification/packaging, seven-day artifacts | Historical build evidence only. Keep CI deferred in the new fork. Success does not imply a physical-device pass. |
| `.github/workflows/ios.yml` | Full Qualification, manual or `ios-qualification-*` tags, Xcode 16.4, clean dependencies/build tree, Gates 1–6, smoke/static-link checks, app and bundle checks, additional historical transplant probes, 14-day artifacts | Preserve history and useful local verification commands; do not carry old investigation probes into the normal local developer procedure. |

History shows bootstrap CI, scoped recovery gates, delivery restoration, then separation into Fast and Full Qualification. Recovery branch `fa7d916` deliberately skips full app/package stages; a green scoped run cannot establish a complete game build. Full Qualification was not run for the accepted WO33 or WO38 Fast milestones. The public Actions index exposed 142 runs, but individual historical run logs and a complete live API enumeration were unavailable.

Verified reproducibility hazards:

1. The local CMake cache records **4.4.4**, while source pins **4.3.4**. An existing successful local build does not validate the documented pinned toolchain.
2. Default `python3` here is **3.9.6**. Validation uses union annotations and `Path.write_text(newline=...)`, requiring Python **3.10+**; audit runs used existing Homebrew Python **3.14.5**.
3. OpenMW/GL4ES bootstrap has revision/patch fingerprints, but `ios/cmake/apply-osg-patch.cmake` recognizes an already-patched OSG tree by a single `gl4es_GetProcAddress` marker. It does not verify the whole evolving OSG patch. Reusing an old populated OSG source tree can skip newer additions. Fresh materialization is the safest consolidation gate.
4. `OPENMW_REFRESH_PATCHES=1` permits hard-resetting dependency trees. Never run it against the user's working dependency edits during recovery; use an isolated clean build directory/check-out.
5. WO38's `f3ccd53` adds `CMAKE_DISABLE_FIND_PACKAGE_GLIB=ON`, recovering an observed cold OSG configure failure caused by host Homebrew GLib discovery. This is a useful isolated build-only candidate absent from WO33.
6. The local uncommitted ICU triplet change appends `cross_compiling=yes`. It is a plausible host/target configure workaround, not an upstream-qualified patch. Preserve and reproduce its necessity before adopting it.
7. Generated `.xcodeproj` files are outputs with absolute local paths and signing edits. Regenerate them from maintained CMake/bridge inputs; do not make the existing generated project the canonical source.

## Xcode project and iOS 27 lifecycle readiness

The existing generated project contains application target `openmw`, engine library `openmw-lib`, bundled dependency targets, static-plugin/dependency aggregate targets, and `openmw-ios-link-smoke`. `ios/bundle-probe` is a separate historical test application, not the production entry point. The production target is created by the structural OpenMW patch; the app links `openmw_ios_platform`, SDL2/SDL2main when present, GL4ES, and Apple frameworks with `-ObjC`.

The generated project has Debug, Release, MinSizeRel, and RelWithDebInfo configurations. Inspected app optimization levels are respectively 0, 3, s, and 2. ARC is disabled at project level. The CMake cache's `CMAKE_BUILD_TYPE=RelWithDebInfo` does not override Xcode's explicitly selected multi-configuration build; the existing app is in Debug. Signing is enabled for the app, while CI overrides it off. Personal Team identity must stay a local setting.

Verified startup path and migration seams:

1. SDL2 2.32.10's `SDL_UIKitRunApp` calls `UIApplicationMain` using `SDLUIKitDelegate`.
2. `SDLUIKitDelegate` uses `application:didFinishLaunchingWithOptions:` and schedules `postFinishLaunch`, which enters the forwarded application main with SDL's event pump enabled.
3. OpenMW's iOS patch exposes `SDL_main`, logs entry, prepares sandbox/configuration arguments, and enters the engine.
4. SDL's UIKit window implementation creates an `SDL_uikitwindow` with `initWithFrame:`. The audited delegate/window implementation has no scene-connection configuration path.
5. Both the source Info.plist template and existing built app lack a scene manifest. `UILaunchScreen` is present, but it is not scene-lifecycle adoption.
6. The touch overlay tries `UIApplication.sharedApplication.keyWindow` and then connected `UIWindowScene` windows. That fallback is scene-aware lookup, not ownership of a scene lifecycle.

Apple documents that apps built with the latest SDK must adopt the scene lifecycle starting with iOS 27 or fail to launch. This supports an SDK-linked explanation for an older-built IPA running while the new SDK build fails. **The exact cause of this user's crash remains unverified until its exception/call stack and binary identity are captured.** [Apple migration documentation](https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle)

Phase 3 should examine SDL app/scene ownership, main-loop entry, UIWindowScene attachment, foreground/background events, touch-overlay attachment, drawable/FBO recreation, and GLES context lifetime together. A plist-only change would not demonstrate that those paths work. SDL's upstream scene work is recorded against SDL3 3.4; it is useful reference material, not evidence that this pinned SDL2 already supports scenes or that a wholesale SDL3 migration is necessary. [SDL issue #12680](https://github.com/libsdl-org/SDL/issues/12680)

No SDL update, scene delegate, lifecycle workaround, renderer change, or Metal migration was implemented.

## Audit verification performed

| Check | Result |
|---|---|
| Branch/tag/commit graph | 29 cached branch heads, three tags, 203 reachable commits inventoried; ancestry and divergent file sets compared |
| Recommended snapshot | `49f5f0b`, exported from committed objects |
| Later release snapshot | `7dbedda`, exported from committed objects |
| OpenMW patch replay | Baseline: all 15 patches pass `git apply --check` then apply in order; release: all 16 pass |
| GL4ES patch replay | Baseline: all nine patches pass; release: all ten pass |
| Baseline existing host suite | **148 tests passed**, no skips/errors, Python 3.14.5 / Apple Clang 21 |
| Release existing host suite | **168 tests passed**, no skips/errors, same environment |
| OSG patch representation | Existing real-parser/materialization fixtures included in the passing suites; not a fresh complete iOS dependency build |
| Installed toolchain | Xcode 27.1 (`27A9275`), iOS SDK 27.1; CMake 4.4.4 locally |
| Generated app metadata | Read Info.plist, Mach-O build version and UUID; no launch attempted |
| Original checkout preservation | Same pre-existing triplet modification and backup after audit; no source/ref changes made |

Initial test discovery in unprepared temporary exports under system Python 3.9 failed because dependency sources were absent and Python APIs were incompatible. These were setup failures, not passing runs. After preparing pristine pinned dependency sources with the repository's existing patch series and selecting Python 3.14.5, both complete suites passed without changing candidate code. Host tests do not validate UIKit launch, GPU output, signing, or sustained gameplay.

Temporary validation records are under `/private/tmp/openmw-phase1-7oiq2fj4/`: `baseline-prepared-tests.log`, `release-prepared-tests.log`, four ordered-patch logs, and the ref inventory. They are disposable audit working files, not a long-term artifact store. Commands and exact revisions are recorded here so the checks can be repeated.

## Risks, blockers, and acceptance status

| Priority | Finding | Required next action |
|---|---|---|
| Blocker to recovery completion | Public fork not created; live refs/PR API not refreshed | Restore authorized GitHub access, create/verify fork, compare fresh inventory before baseline adoption |
| Blocker to runtime qualification | Legacy SDL2 lifecycle plus SDK 27.1 build; actual startup exception unavailable | Capture exact exception and binary/toolchain identity in Phase 3 |
| High | Most recent build is not most recent device-qualified behavior | Start from WO33; preserve WO38 separately |
| High | Mixed/stale evidence and decision snapshots | Keep immutable references; add one accurate baseline summary instead of merging all coordination history |
| High | Diagnostics forced on despite opt-in claim | Record accurately; explicitly qualify any later gating change rather than assuming normal-build overhead is absent |
| High | Reused OSG source can skip patch updates | Require fresh patch materialization and no inherited build caches for first consolidated build |
| High | IPA installed by user not identified | Match original download hash or binary UUID/build metadata before making provenance claims |
| Medium | Python/CMake mismatch; local ICU workaround | Document exact tool selection and reproduce from clean dependencies |
| Medium | Pause candidate and reduced render scale lack complete qualification | Retain candidates separately; do not promise all touch controls/scales work |
| Medium | Remaining foliage, fog, silhouettes, and horizon problems | Preserve current settings/evidence; defer new causal work to renderer phases |

Phase 1's baseline, patch relationships, evidence distinctions, and consolidation recommendation are documented. Fork creation and live-remote completeness remain outstanding access-dependent checks. [integration-plan.md](integration-plan.md) proposes Phase 2; it is not authorization to execute it. **Stop here for audit review.**
