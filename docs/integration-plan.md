# Phase 2 proposal — Consolidate a traceable local-development baseline

Status: **authorized after access recovery; not executed**. This plan follows the findings in [repository-audit.md](repository-audit.md) and the exact refs in [branch-inventory.md](branch-inventory.md). The subsequent user instruction authorizes Phase 2 after authentication, remote refresh, inventory completion, and baseline revalidation. On 2026-10-25, authenticated API requests and an isolated public Git fetch failed DNS resolution before reaching GitHub. Token validity and permissions remain unverified; cached refs still support WO33, but live inventory completion is blocked. See the [access recovery record](repository-audit.md#access-recovery-verification--2026-10-25). No consolidation or application changes have begun.

## Decision proposed

Create the future development `main` from upstream `codex/wo33-blend-state-transition` at **`49f5f0bd80e83ef87eaebd3f69c07072796738aa`**. Its runtime source is identical to device-qualified **`93f892dd0cf9834259b4cad2045ddb2ef9c53ed9`**, and it preserves the final evidence instead of inheriting stale failure reports.

Keep the published WO38 candidate at `7dbedda156b9ab2de1b23f7119f58a6f6a0d6667` available as a separate recovery reference. Do not wholesale merge WO29's administrative line, WO34, WO37/38, or all open PRs. Preserve original history; make any later adaptations small commits with original source SHAs and validation records.

This choice trades the latest observer and unqualified Pause candidate for the best supported runtime checkpoint. It retains known limitations: SDK 27 lifecycle work, distance/fog defects, incomplete touch qualification, and inherited diagnostics. A baseline is a reproducible reference, not a declaration that the application is finished.

## Step 1 — Finish recovery and preserve refs

Prerequisite: restore working authorized GitHub access. The audit could read cached/public evidence and local Git objects but could not create the requested fork or refresh remote refs.

After audit approval:

1. Create or verify the user's public fork of `arjunyerevan95-dot/OpenMWiOS`. Do not publish credentials, local build products, game assets, or working-directory files.
2. Fetch all upstream branch/tag refs and all 21 observed PR heads, including external #21, into an isolated recovery checkout. Paginate the live API for all PR states and compare its result with the inventory. Investigate any new/deleted/moved heads before adopting the recommendation.
3. Record original remote URLs, full SHAs, PR base/head identities, and a dated ref manifest. Preserve historical refs in the fork or a Git bundle; a default-branch-only fork is insufficient preservation of unmerged branches.
4. Keep `main`'s original README commit traceable. Verify it is an ancestor of the selected baseline, so the fork's original `main` can advance without history rewriting. Do not force-push, rebase, squash, or delete upstream branches.
5. Preserve the existing adjacent checkout and its ICU edit. Establish a clean checkout from committed objects for consolidation; do not turn its generated project/cache into the canonical repository.

Verification: all recovered refs have an inventory entry; the selected baseline and release refs resolve to the audited SHAs; original commits remain reachable; no unexpected source files are copied from the dirty worktree.

## Step 2 — Establish the baseline with minimal changes

A short-lived `audit/consolidate-baseline` branch is justified for reviewing the initial build/documentation adjustments. Start it at `49f5f0b`, with all ancestors intact. Promote it to the fork's `main` only after the Phase 2 checks pass. This is a temporary review branch, not a permanent parallel development line.

| Change or source | Proposed disposition | Verification |
|---|---|---|
| Existing cumulative history through WO33 | Retain as-is; no duplicate PR cherry-picks | Ancestry and product-tree comparison to `93f892d` |
| WO33 final evidence `49f5f0b` | Included in selected starting point | Diff outside `Evidence/` is empty versus qualified source |
| WO31 final evidence `123ae04`, WO34–36 negative results, later acceptance reviews | Preserve original refs and link immutable evidence from a concise current baseline document | Each claim names its source commit and actual tested binary |
| WO38 cold-build recovery `f3ccd53` | Candidate for isolated adoption: `CMAKE_DISABLE_FIND_PACKAGE_GLIB=ON` plus independent test; credit original commit | Fresh OSG configure, required plugins retained, no renderer/default changes |
| Local ICU `cross_compiling=yes` workaround | Preserve as a local candidate; adopt only if clean Apple Silicon reproduction demonstrates need | Capture configure failure, host/target distinction, minimal justified fix, repeat dependency build |
| WO38 Pause fix `457ab88` | Keep separate; no automatic production adoption | Later focused physical short-tap, long-press, cancellation, and repeated-input checks |
| WO37/38 target observer | Retain reference branch only | Its missing coverage/depth/sky proof is not addressed by branch consolidation |
| WO34 terrain-radius change | Exclude from development baseline | Confirm `0016-ios-cover-perspective-frustum-terrain.patch` absent |
| PR #21 mod archive | Exclude pending archive/source and behavior review | Do not treat the visible installation instructions as engine-fix evidence |
| Old CI workflows/probes | Preserve in history; leave Actions deferred | No automated build dispatch during consolidation |

For an adapted patch, record an `Upstream-commit:` trailer and explain precisely which files/hunks were carried over. Use `cherry-pick -x` only for a whole commit whose entire contents are appropriate. In particular, do not import WO38-specific “successful build” reports as evidence that a newly assembled WO33-based tree has been built.

Replace misleading current-state guidance with a short accurate entry point in the new baseline. Keep historical work orders/reviews as historical records; do not erase them or resume WO39 merely because an inherited document says ACTIVE. The current roadmap and user-reviewed scope govern this modernization effort.

Verification: every new changed line belongs to recovery, build reproducibility, or documentation; all existing runtime behavior changes are traceable to the selected upstream tree. No lifecycle or renderer fix is part of this step.

## Step 3 — Define and verify the local build contract

Document one supported setup before promising reproducibility:

- Xcode 27.1 / iPhoneOS 27.1 on the inspected Mac, physical arm64 iPhone, deployment minimum 16.3 initially.
- Preserve exact engine, OSG, GL4ES, ios-cmake, LuaJIT, and vcpkg pins from the audit.
- Use the pinned CMake 4.3.4 unless a separately recorded compatibility decision intentionally adopts the existing 4.4.4. Do not silently equate them.
- Select Python 3.10+ explicitly, including subprocesses that invoke `python3`. The audit passed with existing Python 3.14.5; the system 3.9.6 was insufficient.
- Document Ninja, Git, compiler tools, autoconf/automake/libtool/pkg-config, and relevant FFmpeg assembler tools. Resolve the pinned x86_64 ShellCheck versus Apple Silicon host explicitly.
- Retain release-built static vcpkg libraries initially; explain that app Debug symbols/optimization do not make every dependency a Debug library.
- Keep Personal Team and bundle identifier local. Preserve CMake as the source of generated projects and signing settings rather than hand-maintaining generated `project.pbxproj` files.

Use fresh dependency/build directories for the first run. This avoids the OSG marker-only patch guard accepting an old populated source tree and avoids importing the user's unqualified ICU workaround accidentally. Never reset the user's existing dependency trees to accomplish this.

The future local procedure should be based on the existing commands, with verified tool selection and any approved build-only adaptation:

```sh
./scripts/bootstrap.sh
./scripts/validate-source.sh
./scripts/build-ios.sh
python3 -m unittest discover -s validation -p 'test_*.py'
xcodebuild -project build/ios/OpenMW.xcodeproj -target openmw \
  -configuration Debug -sdk iphoneos \
  CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO
```

These are a **procedure to qualify in Phase 2**, not a claim this full Xcode 27 build was executed during the audit. Source validation has additional tool requirements; record them. Preserve useful static archive/registrar, link-manifest, bundle-layout, and resource checks from the existing scripts. Debug validation should prove usable app symbols and a matching dSYM; Release should prove the intended optimized configuration. Avoid redundant full builds unless a failure or change requires them.

The audit already established a useful reference: 15 OpenMW and nine GL4ES baseline patches apply in order, and all 148 baseline host tests pass on prepared sources. The new consolidated tree must independently retain those results. Host tests alone cannot replace compilation/linking or iPhone testing.

Verification record for the first clean build should contain source SHA, dependency/patch hashes, tool versions, selected configuration, relevant CMake settings, source-validation output, link/bundle results, Mach-O UUID, SDK/minimum OS, and dSYM identity. Keep personal signing identifiers and bulky binaries out of public documentation.

## Step 4 — Separate diagnostic policy from renderer changes

The audit found forced diagnostics in bootstrap despite a prior opt-in claim. Initially preserve the exact recovered runtime source and document this fact so baseline comparisons remain meaningful.

Before presenting the consolidated branch as a normal Release/performance baseline, make an explicit decision: either retain the inherited instrumentation with that limitation clearly stated, or review a small, separate change that makes diagnostic enablement controllable and off for normal Release runs. Such a change needs disabled-path and enabled-path checks and subsequent device comparison; it is not already qualified by WO33's opt-in statement. Do not redesign probes or alter rendering state as incidental cleanup.

Likewise, retain the source patch stack initially rather than deleting diagnostics embedded in dependencies simply because they look unnecessary. Separating those patches safely belongs in a focused reviewed change, not an unverified bulk removal.

## Phase 2 completion criteria

- Public fork and refreshed inventories are recorded; upstream history and the selected/restorable reference points remain available.
- `main` derives from `49f5f0b` without rewriting original commits; any build-only additions identify their sources.
- Repository entry documentation correctly describes the current baseline, historical evidence, dependencies, and known limitations.
- A clean local developer procedure regenerates Xcode projects and compiles the app with the selected Xcode 27 toolchain.
- Existing source/patch tests and relevant link/bundle checks pass on that exact tree; Debug symbols are usable.
- Diagnostics behavior is documented accurately; unqualified renderer/touch experiments are not silently promoted.
- No CI/distribution/Metal/native-launcher infrastructure is introduced.

Successful launch on iOS 27 is **Phase 3's** acceptance gate. A known lifecycle launch failure does not justify concealing a Phase 2 build failure, nor should a successful build be described as a successful launch.

## Concrete handoff to Phase 3, after Phase 2 review

Prepare a separate `fix/ios27-lifecycle` branch only when implementation is authorized. First capture the actual startup exception and stack, the installed executable UUID, SDK/minimum OS, built Info.plist, and whether `SDL_main` was reached. Compare the known-working original IPA's metadata if available. The existing local Debug app UUID is recorded in the audit for correlation, not assumed to match the future build.

Then evaluate the smallest maintainable scene integration at the SDL/UIKit boundary: application/scene ownership, a single intended window scene, SDL main-loop timing, foreground/background events, touch attachment, drawable/FBO handling, and GLES context lifetime. Compare a pinned SDL update or explicit patch with a narrow app integration; do not preselect SDL3 or a plist-only workaround without source and runtime evidence.

Acceptance must include Xcode Run, SDL initialization, main menu, entering the world, background/resume, and absence of lifecycle crashes on the physical device. Retain GL4ES/GLES and game logic. Renderer correctness, distant fog, and view-distance optimization remain later phases, with no lowering of visual quality to mask faults.

**This document ends at a proposal. No Phase 2 consolidation or Phase 3 implementation has been performed.**
