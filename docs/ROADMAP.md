# OpenMWiOS – Development & Modernization Plan

**Project:** OpenMWiOS Modernization & Renderer Stabilization  
**Upstream:** https://github.com/arjunyerevan95-dot/OpenMWiOS  
**Target:** iOS 27, physical iPhone  
**Development environment:** Codex, Git, Xcode 27, LLDB  
**Primary goal:** A stable, graphically correct and performant native OpenMW experience on iPhone.

---

## 1. Project Vision

Transform the existing experimental OpenMWiOS port into a maintainable, reliable and performant iOS application.

The project should remain as close as practical to upstream OpenMW rather than becoming a separate engine rewrite.

Primary objectives:

1. Establish a clean and maintainable repository.
2. Enable reliable local builds and debugging using Xcode 27.
3. Correct existing rendering defects.
4. Preserve and improve distant fog.
5. Achieve the highest practical exterior view distance.
6. Optimize performance, ideally targeting stable 60 FPS on capable devices.
7. Preserve compatibility with existing Morrowind game data and OpenMW functionality.

Correctness and stability take priority over aggressive performance optimizations.

## 2. Technical Decisions

The following decisions have already been made:

| Topic | Decision |
|---|---|
| Development agent | Codex |
| Repository | Public GitHub fork |
| Source control | Clean main branch and short-lived feature branches |
| Primary build system | Local Xcode 27 |
| Testing hardware | Physical iPhone |
| Debugging | Xcode, LLDB, device logs |
| iOS Simulator | Not planned |
| GitHub Actions | Deferred |
| IPA distribution | Deferred |
| Apple Developer Program | Not required; use free Personal Team |
| SideStore | Not needed during local development |
| Rendering backend | Preserve existing GL4ES/OpenGL ES initially |
| Metal | Future research only |
| Graphical launcher | Future enhancement, outside current scope |

Do not introduce paid services or unnecessary infrastructure.

## 3. Phase 1 – Repository Recovery and Audit

**Goal:** Identify the most complete, functional and maintainable source state.

### Tasks

1. Fork the upstream repository.
2. Inspect all remote branches, open pull requests and commit histories.
3. Analyze relationships and dependencies between development branches.
4. Identify the source commit corresponding to the known-working IPA, if possible.
5. Inspect existing build scripts and dependency versions.
6. Identify unfinished experiments, duplicate changes and conflicting patches.
7. Establish which changes have actually been tested on physical devices.

Pay particular attention to the existing exterior-renderer diagnostic pull requests:

- PR #17 – Exterior Diagnostics
- PR #18 – Exterior Renderer Diagnostics
- PR #19 – Blend-State Transition
- PR #20 – Terrain Frustum / Distance Horizon

Do not assume the newest commit is the best starting point.

Do not blindly merge all open pull requests.

### Deliverables

- `docs/repository-audit.md`
- `docs/branch-inventory.md`
- `docs/integration-plan.md`

### Acceptance Criteria

- The best available starting point has been identified.
- Relevant patches and their dependencies are documented.
- Unverified experiments are distinguished from confirmed fixes.
- A safe consolidation strategy exists.

## 4. Phase 2 – Repository Consolidation

**Goal:** Establish a clean development baseline without losing working code.

### Tasks

1. Create a clean `main` branch from the selected viable baseline.
2. Preserve important upstream history and source references.
3. Integrate verified upstream patches in dependency order.
4. Avoid integrating incomplete diagnostic experiments as production fixes.
5. Establish short-lived branches such as:
   - `fix/ios27-lifecycle`
   - `fix/vegetation-rendering`
   - `fix/distant-rocks`
   - `fix/fog-consistency`
   - `perf/view-distance`
6. Document third-party dependencies and build requirements.
7. Create a reproducible local build procedure.

Use a separate integration branch only if necessary.

Do not rewrite or delete upstream branches.

### Acceptance Criteria

- Repository structure is understandable.
- Source history remains traceable.
- Xcode project generation and compilation are reproducible.
- A known baseline can be restored.

## 5. Phase 3 – iOS 27 Lifecycle Migration

**Goal:** Make the locally compiled application launch correctly on iOS 27.

### Existing Situation

The project reportedly compiles successfully under Xcode 27.

However, launching the compiled application on the iPhone fails with an application lifecycle-related crash.

A separately distributed IPA from upstream runs successfully on the same device.

This indicates that build success and runtime compatibility must be investigated separately.

### Tasks

1. Capture and analyze the actual startup exception and call stack.
2. Inspect the SDL2 iOS integration and UIKit lifecycle implementation.
3. Verify the iOS 27 SDK requirements.
4. Investigate:
   - `UIApplicationDelegate`
   - `UISceneDelegate`
   - `UIWindowScene`
   - `Info.plist`
   - SDL window creation
   - OpenGL ES context initialization
   - Application foreground/background transitions
5. Determine whether SDL2 should be patched, updated or integrated differently.
6. Implement the smallest maintainable lifecycle correction.
7. Test application launch and resume behavior on the physical iPhone.

Avoid unnecessary changes to OpenMW game logic.

Design the lifecycle integration so a native launcher could be added later without another major restructuring.

### Acceptance Criteria

- Application builds with Xcode 27.
- Application launches using Xcode Run.
- SDL initializes successfully.
- OpenMW reaches the main menu.
- The player can enter the game world.
- Backgrounding and returning to the application works.
- No lifecycle-related crashes occur during normal testing.

## 6. Phase 4 – Local Development and Debugging Environment

**Goal:** Establish a fast and reliable development loop.

### Development Workflow

1. Codex analyzes a problem and modifies the source.
2. Xcode builds the application locally.
3. Xcode installs and launches the application on the connected iPhone.
4. Breakpoints, LLDB and logging are used to inspect runtime behavior.
5. The user validates graphical results and gameplay.
6. Findings are documented.
7. Codex creates the next focused patch.

### Build Configurations

**Debug**

- Suitable debug symbols
- Low or moderate compiler optimization
- Optional renderer diagnostics
- LLDB compatibility
- Detailed crash information

**Release**

- Production compiler optimizations
- Minimal diagnostic overhead
- Representative gameplay performance
- Suitable for performance measurements

Keep the two configurations separate.

### Developer Experience

Document:

- Xcode setup
- Personal Team signing
- iPhone deployment
- Required Morrowind data files
- Debugging with LLDB
- Common build and startup problems

### Acceptance Criteria

A developer can clone the repository, follow the documentation, build the application and debug it on an iPhone without a paid Apple Developer account.

## 7. Phase 5 – Renderer Diagnostics

**Goal:** Establish the root causes of rendering problems before implementing fixes.

### Confirmed User Observations

**Vegetation – Default configuration**

Tree foliage appears and disappears depending on camera direction, including at close range.

**Vegetation – Modified configurations**

Certain view-distance or fog configuration changes cause tree crowns to display foliage textures belonging to other tree types.

These are recognizably different tree textures, not random environmental textures.

The problem is camera-direction dependent and occurs even at close range.

**Distant rocks**

Some distant rocks remain unnaturally prominent relative to surrounding fog.

Their visual appearance is inconsistent with the rest of the landscape.

**Distant fog**

Distant fog is functional and should be preserved.

**View distance**

Increasing the viewing distance improves the visual experience but can change how vegetation rendering defects manifest.

### Previous Configuration Experiments

| Test | Change | Result |
|---|---|---|
| Original | Default configuration | Foliage disappears/reappears |
| A | Increased distance, modified fog, paging on | Different tree textures |
| B | Original distance/fog, paging off | Foliage disappears/reappears |
| C | Increased distance only | Different tree textures |
| D | Modified fog distances only | Different tree textures |
| E | Distant fog disabled, original distance | Different tree textures |
| F | Distant fog disabled, increased distance | Different tree textures |

Disabling antialiasing-related options did not resolve the problems.

### Diagnostic Scope

Investigate:

- OpenSceneGraph state transitions
- GL4ES state caching
- Texture binding and texture units
- Texture and shader sampler associations
- Rendering batches and draw-call ordering
- Alpha testing and blending
- Depth buffer handling
- Camera projection matrices
- Fog shader uniforms and calculations
- Terrain and object culling

These are hypotheses, not proven root causes.

### Diagnostic Requirements

Create targeted instrumentation capable of recording relevant draw-call and OpenGL state information.

Compare requested rendering state with actual state where possible.

Use the existing upstream diagnostic PRs as references, but verify their correctness and applicability before integrating them.

Avoid excessive logging in normal builds.

## 8. Phase 6 – Rendering Correctness

**Goal:** Eliminate the known rendering defects without reducing visual quality as a workaround.

### Vegetation

- Fix disappearing foliage.
- Fix incorrect tree texture assignments.
- Ensure stable rendering when rotating the camera.
- Validate close-range and distant vegetation.
- Test different tree models and environmental conditions.

### Distant Rocks

- Fix incorrect visual appearance of distant rock geometry.
- Ensure consistent shader and texture behavior.
- Ensure distant rocks receive appropriate fog treatment.

### Fog

- Preserve distant fog.
- Ensure fog behaves consistently across terrain, rocks, vegetation and other world geometry.
- Avoid disabling fog to conceal unrelated renderer errors.

### Render-State Stability

Investigate and correct any verified errors in OpenSceneGraph, GL4ES or OpenMW's renderer integration.

Prefer isolated, testable patches.

### Acceptance Criteria

- Vegetation textures remain correct regardless of viewing direction.
- Vegetation no longer disappears unexpectedly.
- Distant rocks render consistently.
- Distant fog remains functional and visually coherent.
- Indoor rendering does not regress.
- The application remains stable during normal gameplay.

## 9. Phase 7 – Maximum Practical View Distance

**Goal:** Achieve a high-quality distant landscape with the greatest practical view distance on iPhone hardware.

This is an optimization goal, not a workaround for renderer defects.

### Tasks

1. Establish performance baselines at multiple viewing distances.
2. Measure CPU and GPU costs.
3. Investigate terrain rendering and object-culling efficiency.
4. Identify excessive draw calls and rendering overhead.
5. Optimize geometry handling and rendering state changes.
6. Evaluate texture memory and GPU bandwidth usage.
7. Test different view-distance settings and weather conditions.
8. Preserve atmospheric distant fog.
9. Provide configurable graphics presets where useful.

### Priorities

1. Correct rendering
2. Stable gameplay
3. High practical viewing distance
4. Smooth frame delivery
5. Reasonable battery and thermal behavior

### Performance Target

Aim for stable 60 FPS on sufficiently capable devices where feasible.

Measure actual frame times rather than relying only on average FPS.

Do not sacrifice rendering correctness to reach a numerical performance target.

## 10. Future Enhancements – Outside Current Scope

These are possible future directions and must not delay the current development milestones.

### GitHub Actions

Automated builds, reproducible artifacts and optional CI testing.

### SideStore

Free IPA signing and installation for users who do not develop through Xcode.

### Native iOS Launcher

Potential SwiftUI interface for:

- Editing `settings.cfg`
- Managing `openmw.cfg`
- Activating/deactivating ESM and ESP plugins
- Plugin load order
- Mod import and management
- Graphics presets
- Log viewing and diagnostics

### Metal Research

Evaluate alternative rendering architectures only after the current application is stable.

Potential investigations:

- GL4ES with ANGLE/Metal
- A dedicated Metal renderer
- A broader rendering abstraction

Do not initiate a Metal migration as part of the current milestones.

## 11. Development Rules for Codex

1. Inspect the relevant code before modifying it.
2. Preserve working features.
3. Prefer small and reviewable changes.
4. Distinguish hypotheses from verified causes.
5. Never claim device-tested success without actual device evidence.
6. Maintain traceability to upstream OpenMW and OpenMWiOS.
7. Avoid permanent modifications to upstream dependencies when maintainable alternatives exist.
8. Document significant architectural decisions.
9. Avoid introducing unnecessary infrastructure.
10. Keep renderer diagnostics separate from production behavior.
11. Do not reduce graphical quality to hide bugs.
12. Do not work on deferred features without explicit approval.

## 12. Initial Codex Assignment

Start with Phase 1: Repository Recovery and Audit.

Inspect the upstream repository and identify:

- The most complete source branch
- The likely provenance of the working IPA
- The relationship between development PRs
- Which changes are verified and which remain experimental
- Dependencies required for an Xcode 27 build
- The safest strategy for consolidating the repository

Produce the audit documents and an integration recommendation.

Then proceed to implement the clean baseline and investigate the iOS 27 startup failure.

The immediate milestone is:

**Build and launch OpenMWiOS on a physical iPhone using Xcode 27, with full local debugging available.**
