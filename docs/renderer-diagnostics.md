# Renderer diagnostics and performance baseline

This change starts from main `92fae65b55ce327bc25acddb2fba27d93f16eb40`, the
user-validated iOS 27 lifecycle migration. It makes inherited renderer probes
opt-in. It does not establish an FPS improvement or diagnose the reported
performance difference from the distributed IPA. That IPA's exact sources,
build configuration and settings have not been established.

## Configuration and outputs

`OPENMW_IOS_RENDERER_DIAGNOSTICS=1` enables the existing renderer probes.
Unset, `0`, empty and all other values disable them. This applies equally to
Debug and Release builds. The setting is read once, at first use, and remains
fixed for the process lifetime. Stop the app and launch again after changing it;
backgrounding/resuming is insufficient. No generated project edits are required.

In Xcode:

1. Select the **openmw** scheme and your physical iPhone.
2. Open **Product → Scheme → Edit Scheme… → Run → Arguments**.
3. Under **Environment Variables**, add `OPENMW_IOS_RENDERER_DIAGNOSTICS` with
   value `1` and check its checkbox to enable diagnostics.
4. For normal gameplay, remove/uncheck that row or set its value to `0`.
5. Stop the running process, then use **Product → Run**. Launch through Xcode
   for both comparison runs: a launch from the Home Screen does not inherit
   Xcode's scheme environment.

Effective configuration is written once per startup to
`Library/OpenMW/startup.jsonl` with milestone `renderer_diagnostics_config` and
`enabled=0` or `enabled=1;source=environment;restart_required=1` in its detail
(the source/restart fields are present in both cases). Inspect the newest
matching timestamp, since this startup file appends across launches.
It is file-backed; absence of console output is not evidence that it is off.
When paused under LLDB, the optional direct check is:

```text
expr -- (int)openmw_ios_renderer_diag_enabled()
```

If LLDB cannot resolve the function in an optimized build, use the startup file.
Resume before measuring; debugger expression evaluation is not a measurement.

| Output | Location / behavior |
|---|---|
| Effective configuration and ordinary startup/lifecycle milestones | `Library/OpenMW/startup.jsonl`; retained in both modes |
| WO31–33 renderer records | `Documents/OpenMW/renderer-diagnostic.jsonl`; enabled sessions truncate the old file, create a session UUID, retain existing family limits and 256 KiB ceiling |
| WO23 bounded readback and program attachment messages | OpenMW's ordinary `openmw.log` (under the configured log directory, normally `Documents/OpenMW`) and any configured console logger |
| WO17 original/submitted shader dump and compile status | Standard output, visible in an attached Xcode console; not copied into renderer JSONL |

Disabled runs do **not** create, truncate, append to or remove the renderer JSONL.
A file left by a previous enabled run is stale evidence, not a fresh enabled
session. Archive it before comparing; check its timestamp/contents after the
new run. A missing enabled file is also not proof of a disabled setting: check
the startup record and container write availability.

To retrieve files: **Window → Devices and Simulators** (`⇧⌘2`), **Devices**,
select the iPhone, select OpenMW under **Installed Apps**, then the app actions
menu → **Download Container…**. In Finder, right-click the `.xcappdata` file →
**Show Package Contents**. The paths above are inside `AppData/`. Files exposed
through Files/Finder file sharing include Documents, but not Library.

## Instrumentation audit

Historical design/evidence remains in
[WO31 diagnostic channel](../Evidence/WO-031/diagnostic-channel.md) and
[WO33 blend transitions](../Evidence/WO-033/blend-transition-model.md).
Those records describe the earlier forced-on behavior.

| Layer / probes | Before this change | Disabled path now |
|---|---|---|
| iOS bootstrap and bridge | Bootstrap overwrote the environment with `1`; enabled checks acquired the bridge mutex. Records serialize JSON, write files, maintain texture/fog maps and a 48-event blend ring. | Explicit cached opt-in; all public probe entries return before locks, allocations, thread hashing, image hashing or output. One startup configuration record remains. |
| OpenMW WO31–32 asset/state/fog probes (0013–0015) | Already gated at callers, but the bootstrap forced their gate on. Capture asset identities, image hashes, requested blend/alpha/depth state and fog intent/generations. | Existing guards now observe the off default; observations remain available when enabled. |
| OpenMW WO23 probes (0010) | Ungated five-pixel `glReadPixels` samples at frames 600/1200/1800; up to eight shader attachment logs, plus repeated entry checks. | New 0016 guards readback before frame inspection/GL calls and program logs before matching/formatting. |
| OSG State / BlendFunc | Weak-symbol presence enabled trace formatting at blend boundaries, even if the bridge would discard output. | Check the setting before formatting. WO33 manual blend routing and cache-match reassertion still execute independently. |
| OSG Texture2D | Texture registration hashed image bytes before category lookup and possible rejection. | Return before image inspection/hashing when off. Texture application itself is unchanged. |
| GL4ES WO31–33 | Helpers mostly checked the bridge, but callers scanned texture units and inspected shader strings per draw; blend ingress formatted traces first. | New 0010 guards the diagnostic scans, string searches, trace formatting and category lookup. Helpers retain their own guards. |
| GL4ES WO17 shader dump (0004) | Source-string matching during compilation; bounded to the first qualifying vertex/fragment shader, queries compile status/log and prints source. | Same opt-in before source matching or diagnostic queries; actual shader compilation is untouched. |

**Confirmed work, unmeasured cost:** source inspection proves the hash loops,
per-draw scans, formatting, bridge locking, file I/O and bounded
framebuffer reads execute in the old path. A file/family output cap does not
stop all upstream probe work or subsequent calls. Disabled paths now bypass
that work; inexpensive function calls, symbol checks and cached-boolean branches
remain. Enabled diagnostics intentionally retain their existing collection
behavior, including work after output budgets are exhausted.

**Suspected performance impact:** CPU time, contention, GPU synchronization from
readback and storage latency may affect frame times. Their magnitude, and their
contribution to the IPA comparison, have not been measured on a device.

Ordinary engine errors, startup/context/first-present milestones and lifecycle
logs are retained. They are not the renderer trace channel. Existing upstream
GL4ES `LIBGL_LOGSHADERERROR`, `LIBGL_TEXDUMP`, `LIBGL_FPS` and source-level DEBUG
logging are separate opt-ins and remain unchanged; do not enable them for the
baseline. No new runtime profiler or FPS overlay is introduced.

## Implementation boundaries

Maintained files are the bootstrap, diagnostic bridge, consolidated OSG patch,
its CMake application guard, OpenMW follow-up patch **0016**, GL4ES follow-up
patch **0010**, tests and this documentation. All dependency revisions are
unchanged. The OpenMW/GL4ES historical patches remain intact.

The OSG patch driver previously considered one routing symbol sufficient to
skip patching. It now verifies that the whole current patch can be reversed in
a dry run. An older/modified tree fails with a fresh-tree instruction instead
of silently keeping forced diagnostic work. It does not reset local sources.

Rendering commands, shader source/conversion, texture binding/state, blend
semantics, fog, terrain, culling, view distance, touch and lifecycle code are
unchanged. Visual parity is required on device; source/host tests cannot prove
it. Existing vegetation, wrong-texture and distant-rock/fog issues remain open.

## Rebuild on the Mac

Close Xcode first. Keep your usual Personal Team and bundle identifier so the
installed app's game data/save container is reused. Back up that container.
The new patch fingerprints require freshly materialized OpenMW and GL4ES,
and OSG must be re-extracted. From the repository root:

```sh
git fetch origin
git switch perf/opt-in-renderer-diagnostics
git pull --ff-only

# Preserve existing sources, local edits and generated projects for inspection.
diag_backup="$(mktemp -d "$PWD/../OpenMWiOS-before-diagnostics.XXXXXX")"
for item in deps/openmw deps/gl4es build/ios build/gl4es-ios; do
    if [ -e "$item" ]; then
        mkdir -p "$diag_backup/$(dirname "$item")"
        mv "$item" "$diag_backup/$item"
    fi
done
./scripts/bootstrap.sh
CONFIGURATION=Release ./scripts/build-ios.sh
open build/ios/OpenMW.xcodeproj
```

This preserves the installed vcpkg dependencies/downloads and LuaJIT cache.
Inspect any dependency edits in the backup before porting them to maintained
patches; do not copy old generated/compiled files into the fresh tree. The
backup is for preservation, not a relocatable Xcode project. If commands fail,
stop and inspect the first error before proceeding. Do not bypass fingerprint
or OSG checks. Re-select **openmw → Signing & Capabilities → your Personal Team**
and the **same Bundle Identifier** used before (or supply the existing
`DEVELOPMENT_TEAM`/`PRODUCT_BUNDLE_IDENTIFIER` to the build script).

## Physical-iPhone validation and comparison

1. In **Edit Scheme → Run → Info**, choose **Release**. The script builds GL4ES
   in Release; use Release for OpenMW/OSG as well. Debug is for debugging, not
   for comparison against a distributed optimized IPA. Record the exact Git
   SHA (`git rev-parse HEAD`), Xcode/SDK versions, iPhone model and iOS version.
2. Run with diagnostics off; verify `enabled=0`. Cold-launch, load the chosen
   save, enter the exterior, rotate the camera through vegetation/smoke/distant
   rocks, return to the menu, background/resume and verify touch controls.
   Compare visuals to the same route with diagnostics on; report any difference.
3. Enable the environment variable, stop and Run again. Verify `enabled=1`, a
   new renderer session and expected asset/upload/draw/fog or blend records as
   the relevant scene is exercised. Targeted records require matching assets
   and exterior fog; not every scene emits every family. Check the WO17 stdout
   and WO23 log samples if investigating those probes specifically.
4. Set `0`, stop and Run again. Verify `enabled=0` and no new renderer JSONL
   writes. No rebuild is necessary when switching this environment variable.
5. For timing, use **the same Release binary** for on/off runs. Keep debugger
   attachment, diagnostic tools and other Xcode runtime checks identical;
   preferably uncheck **Debug executable** for both measurement runs. Keep
   assets/mods, save, weather/time, viewpoint/route, resolution/render scale,
   graphics settings and view distance identical. Do not change fog settings.
6. Use the same measurement tool and capture duration for each run. If only
   visual impressions are available, label them qualitative. For quantitative
   results capture FPS/frame times with an available device profiling tool,
   record median FPS and frame-time percentiles (especially p95/p99) and
   stalls, and retain the raw samples. Do not infer improvement from log size.
7. Use equal warm-up periods, then at least three on/off pairs, alternating
   order. Keep power/charging state, Low Power Mode, brightness and device
   temperature comparable; allow cooling between runs. Measure loading/startup
   separately from steady gameplay, and note whether sampling crosses the
   bounded readback frames or diagnostic budget exhaustion.

Report visual/lifecycle results and measurements for each mode, including any
missing output. A comparison to the old IPA is secondary until its settings and
build provenance are known. Merge waits for physical-device validation.

## Cloud validation

- 159 host tests pass, including the actual cached configuration function
  compiled as C++, and the fully patched GL4ES diagnostic C translation unit
  with enabled/disabled bridge fixtures. Disabled bridge hashing, lookup,
  recording and blend callbacks abort the fixture if reached.
- Source assertions check public bridge early returns and expensive caller
  guards; OSG tests apply the real patch, verify reapplication detection and
  reject a stale tree without writing to it. Existing blend-routing tests pass.
- Complete 16-patch OpenMW and 10-patch GL4ES series apply to clean pinned Git
  snapshots; OSG applies to pinned fixture inputs. Dependency revision checks,
  shell/Python syntax, JSON validation and pinned ShellCheck 0.11.0 pass.
- `scripts/validate-source.sh` remains nonzero on this Linux host because
  `plutil` and Ruby are unavailable. ShellCheck was installed and passed afterward.
  Supplemental Python plist/YAML parsing passes; this does not substitute for
  those platform/tool checks.
- `cmake -S validation -B build/validation` fails at the existing framebuffer
  assertion in `validation/CMakeLists.txt:214`. Reproduced on an unmodified
  archive of main `92fae65`: its multiline regex matches an earlier added line
  through the removed `SDL_GetWindowSize` line in patch 0005. This pre-existing
  validator defect is not changed here; the renderer sizing code is untouched.
- No Xcode build, physical-device run, visual parity result or performance
  measurement is claimed for this change in Cloud.
