# Vegetation investigation: evidence and next device experiment

Investigation base: `86cbd08ce7b41f36bdde71682ac5ea7dbec0cb62` (PR #3 merged).
Branch: `investigate/vegetation-texture-state`.
No renderer correction or additional runtime instrumentation is included.
There is no demonstrated cause yet for the current wrong-species textures or
camera-dependent missing foliage. The following experiment tests the first
unverified state boundary before adding more instrumentation.

## Evidence ledger

The current user's iPhone runs both diagnostic modes. Environmental defects
persist in both; stuttering seemed lower in both. This does not establish an
FPS difference or demonstrate that diagnostics cause the rendering defects.
Disabling paging/AA did not resolve the reported foliage defect. Changes in
view distance/fog correlate with wrong textures, including nearby trees; they
are not proof that fog calculations or distance culling are responsible.

| Record | Established result | Limits / experiments not to repeat |
|---|---|---|
| WO31 | Diagnostic NSString lifetime error caused the initial diagnostic crash; ownership repair passed that boundary. Later capture had 22 OpenMW records and no GL4ES/R2 records. | Empty GL4ES output did not prove absence of drawing. No vegetation correction established. |
| WO32 | Smoke asset/alpha intent arrived with GL4ES blend disabled. Routing direct OSG mode/blend calls through GL4ES alone failed its device prediction. | `tx_bc_moss.dds` was DXT1/RGB and opaque at the sampled shader boundary. That sample did not prove that this asset required alpha, nor identify the currently defective tree. |
| WO33 | OSG cache-match suppressed blend reconciliation. Reassertion produced 55 GL4ES ingress calls and all four sampled smoke draws had blend=1; user confirmed smoke/spell/foliage transparency improvement. | Preserve this correction. The old opaque-card fix does not establish correctness of all current foliage textures or camera angles. |
| WO34 | Correcting aspect-blind terrain coverage did not fix white gaps, blue band or black distant silhouettes. | That specific terrain-radius explanation failed for those distance symptoms; not a blanket disproof of all culling defects. Do not import the rejected patch. |
| WO35 | Proven sky blending changed some silhouette fading, but blue/white cutoff persisted. | Configuration-only experiment; no evidence for a wrong-tree-texture fix. |
| WO36 | Paging at 7168 did not fix cutoff. At 16384, coverage increased but the defect recurred at the farther boundary. | Moving the boundary was not a correction. Do not repeat distance/paging sweeps. |
| WO37 | Request-based pixel observer remained unarmed in two device sessions. Auto-first-exterior fallback subsequently failed to build due to GLib discovery. | No trustworthy intended-draw/native-pixel correlation. Missing records were a capture failure. |
| WO38 | Cold OSG build recovered; observer built, then a Pause correction built. Final report still has device Pause and pixel attribution pending. | Build success is not attribution. First-exterior capture cannot be matched to screenshots taken after moving elsewhere. Do not import the observer/touch changes wholesale. |

WO31–33 sources: `Evidence/WO-031/report.md`, `Evidence/WO-032/report.md`,
`Evidence/WO-032/device-capture-analysis.md`, `Evidence/WO-033/report.md`,
`Evidence/WO-033/blend-transition-capture.md` in this repository. Original raw
attachments are referenced by hashes in those records; they were not available
here for independent image/log reanalysis. Later evidence was read from these
preserved branch snapshots, including their reports and device/capture records:

| WO | Snapshot commit |
|---|---|
| 34 | `c82542b5daa8f70764818d0058ad47e1f541efa9` |
| 35 | `0b563307a32688a4aa5feddb6587f329f13c67b0` |
| 36 | `4f6cfc62ced645d4465f401520a1dfaca5e65ab7` |
| 37 | `7c17095ff876909e31e4c7e63702fff52b237373` |
| 38 | `7dbedda156b9ab2de1b23f7119f58a6f6a0d6667` |

For example, `git show c82542b:Evidence/WO-034/report.md` reads the preserved
report without applying its code. Historical stop/budget instructions describe
those experiments, not new authority to change renderer behavior.

## Verified source paths

Pins remain OpenMW `f4bec41444214a7903bebd178389ca22ca13f646`, OSG
`01cc2b585c8456a4ff843066b7e1a8715558289f`, GL4ES
`c9895df34cd466c23bc60c2bd3db3d87e98fcbe7`, with the main patch stacks.

| Boundary | Relevant files/functions | Observation |
|---|---|---|
| Asset and material intent | OpenMW `components/nifosg/nifloader.cpp`: `attachExternalTexture`, `attachTexture`, `handleAlphaTesting`; `components/resource/imagemanager.cpp` | VFS image identity becomes an OSG Texture2D on a specified material unit; alpha test/reference comes from the material. ImageManager caches by path. |
| Shader and sampler intent | `components/shader/shadervisitor.cpp`: texture interrogation, `diffuseMap`, alphaRef, `new osg::Uniform(name.c_str(), unit)` | Diffuse sampler unit and alpha shader semantics must be read from the effective drawable state, including inherited StateSets. Filename alone does not establish alpha intent. |
| Camera-dependent state application | OSG `src/osgUtil/RenderLeaf.cpp`: `render`; `src/osg/State.cpp`: `apply`; `include/osg/State`: attribute stacks, `setActiveTextureUnit` | Traversal/order changes which StateGraph transitions and cache matches occur. RenderLeaf applies effective state then calls `_drawable->draw(renderInfo)`. Camera dependence can expose stale state without a camera-math defect. |
| Texture binding and lifetime | OSG `src/osg/Texture2D.cpp`: `apply`; `src/osg/Texture.cpp`: `TextureObject::bind`, object allocation/deletion | `TextureObject::bind()` calls unprefixed `glBindTexture(_profile._target, _id)`. Allocation/deletion similarly call unprefixed GL functions. OSG's dynamic active-unit function goes through patched GetProcAddress. |
| GL4ES logical binding | `src/gl/texture_params.c`: `gl4es_glActiveTexture`, `gl4es_glBindTexture`, `gl4es_glDeleteTextures` | Logical `texture.active` and `texture.bound[unit][target]` differ from native active/bound state. A same-object bind can return early; 2D binding is deferred using `bound_changed`. Deletion clears logical references and `actual_tex2d` entries. |
| Native texture realization | `texture_params.c`: `realize_textures`, `realize_1texture` | `gltexture_t.texture` is the logical name, `glname` the native name; `actual_tex2d[]` is a cache, not a GL query. Realization conditionally changes native active unit/binding. |
| Program/uniform realization | `src/gl/fpe.c`, `src/gl/uniform.c` | Logical and native program can differ; `glstate->gleshard->glprogram`, sampler `req_tu`/`act_tu`, and native uniform value must be correlated. Never equate logical program IDs with native IDs by assumption. |
| Submission | `src/gl/drawing.c`: `glDrawElementsCommon`; `src/gl/listdraw.c`: replay; OSG `Geometry::drawImplementation` | Common path realizes textures then submits native draws, with separate replay/instancing paths. The decisive snapshot is immediately before the actual native draw, after realization. |

### Strongest source-level lead

OSG's direct `glBindTexture` route is not replaced by the current OSG patch.
GL4ES `src/gl/attributes.h` makes `AliasExport` a declaration on Apple, while
`gl4es_glBindTexture` is a separate definition. The bundled GL header declares
`glBindTexture` without remapping it. Thus there is a concrete opportunity for
OSG's native binding changes to bypass GL4ES logical state, similar in structure
to the historical blend split. The exact device's final symbol resolution,
executed route and first mismatched foliage draw remain to be captured.
A mixed route alone is not proof of the visible defect.

A second source lead is `realize_textures`: inside its `i` loop it selects the
texture target from `enable.texture[texture.active]`, then reads `bound[i][tgt]`.
This may be significant with different enabled targets across units. If all
relevant units use 2D, that difference may be immaterial. Do not change the
index without a failing draw demonstrating the precondition and mismatch.

## Ranked hypotheses and distinguishing predictions

1. **Split OSG/native/GL4ES texture state (highest priority).** OSG binds an image
   on native unit B while GL4ES believes unit A or a different texture is active;
   subsequent cached realization or a sampler reads a preceding tree's texture.
   The wrong texture's alpha can also erase foliage. Prediction: intended
   image/unit, wrapper state and native sampler binding first diverge on the
   same draw; correlate direct native bind caller with the missing wrapper.
2. **GL4ES realization or sampler synchronization.** Logical intended image is
   correct but native binding/program sampler is stale, including the target
   index lead above. Prediction: wrapper ingress is correct, mismatch appears
   only during realization/program change; capture native program, sampler and
   requested/actual units. Uniform location numbers are program-specific.
3. **Object reuse or stale identity mapping.** OSG object/native name reused for
   another image, or diagnostic maps still label an old object. Prediction:
   same numeric name gains a new image/upload across delete/recreate or storage
   replacement. Need context plus lifetime, not numeric name alone. Current
   diagnostic maps are not lifetime-aware and do not prove this engine bug.
4. **Material alpha / shader variant / UV state.** Intended image and native
   sampler binding agree but actual discard/alphaRef or texture coordinates are
   wrong. Prediction: correct bindings on good/bad draws with different alpha
   semantics or geometry/UV data. This can hide leaves; it explains a genuinely
   different species less directly than wrong texture selection.
5. **Cull/coverage or asset/mod conflict.** If the intended drawable never reaches
   submission in the bad angle, inspect traversal first. If intended image is
   already wrong at NIF/VFS loading, inspect assets and overrides. Neither an
   absent capped log nor a screenshot alone proves a missing draw or wrong asset.

## Existing diagnostic limits

PR #3 provides explicit opt-in and inexpensive disabled paths, not extra
native-state attribution. Current foliage target selection uses broad name
heuristics (`moss`, `fern`, `leaf`, `flora`, `tree`). It can select the wrong
representative for this investigation. The asset category also recognizes
`kelp`, while target selection does not. No hit is therefore not proof of no draw.

The current common-draw probe picks the first recognized bound target and stops
scanning. It does not prove the active shader samples that unit. It records
logical GL4ES texture/program/state, not queried native GLES bindings or the
intended OSG drawable. Targeted draws require matching exterior-fog state and
are limited to four hits per target per process; the whole file has a 256 KiB
cap. A later bad camera angle may never be recorded. Hash-to-name registration
can conflate identical image bytes; native/OSG names can be reused. Shader
substring flags are not proof of an executed alpha-discard path.

Do not repeat WO37's unreliable first-exterior screenshot matching. The next
capture is manually armed at the chosen tree via LLDB. Do not add per-frame
readbacks or a broad trace until this bounded route test has been attempted.

## Physical iPhone procedure

### 1. Prepare a reproducible target, without a new build first

Use the existing PR #3/main binary. Keep the working Bundle Identifier and
Personal Team; do not reinstall under a new identifier or delete app data.
Keep fog, view distance, paging, AA, mods and render scale unchanged throughout.
Record the source SHA, configuration, iPhone/iOS and save identity. Pick one
nearby defective tree and save there. Establish a repeatable small camera
rotation A (correct) → B (wrong/missing) → A, recording images/video and which
physical tree is being followed. If no good angle exists, use a second known
correct tree as control and label it separately.

In Xcode Edit Scheme → Run, enable **Debug executable** and set
`OPENMW_IOS_RENDERER_DIAGNOSTICS=1`. Stop and Run again. Load the target save.
Copy `Documents/OpenMW/renderer-diagnostic.jsonl` and the newest configuration
record from `Library/OpenMW/startup.jsonl` via Devices and Simulators (⇧⌘2) →
Installed Apps → OpenMW → Download Container → Show Package Contents → AppData.
Look for the relevant `r1.asset`/OSG texture registration identity, not an old
numeric texture from WO32. This is asset discovery only; the first four draw
records must not be attributed to the later screenshot without a matching stop.

### 2. Verify the actual route (first requested LLDB result)

Pause after loading the tree, then enter:

```text
image lookup -n glBindTexture
image lookup -n gl4es_glBindTexture
breakpoint set -n 'osg::Texture::TextureObject::bind()'
continue
```

On the breakpoint:

```text
thread backtrace
frame variable this
expression -- this->_id
expression -- this->_profile._target
```

Record the breakpoint ID printed by LLDB. Inspect the caller `Texture2D::apply`
frame (`frame select N`, using its number in the backtrace), and inspect `this`
and its image filename with `frame variable *this`. Where available:

```text
expression -- this->getImage()->getFileName().c_str()
```

Record the image path and texture object address. Stop after a few samples if
these are unrelated assets; do not claim a specific tree from a generic moss
name. For a matching image, use the bind breakpoint's condition `this->_id == N`
(with the observed numeric N) for subsequent stops in this session. Names may
change after restart, so rediscover them then.

At the selected TextureObject::bind frame, `disassemble --frame` shows the
actual call target. Use `thread step-inst` to follow that call (not `thread
step-over`), then `image lookup --address $pc` and `thread backtrace` to establish
whether it enters native GLES directly or `gl4es_glBindTexture`. A symbol lookup
alone is only linking evidence, not executed-route evidence.

If breakpoints have zero locations or `this`/members are unavailable, report
that exact output. Do not guess register contents for a C++ object. Only then
rebuild GL4ES and OpenMW/OSG with debug symbols, e.g. use
`CONFIGURATION=RelWithDebInfo PRODUCT_BUNDLE_IDENTIFIER=<existing-id>` with the
existing build script and choose RelWithDebInfo under Run. This investigation
is not a performance measurement. No dependencies need version changes.

### 3. Correlate a selected drawable with native submission

This is the follow-up once the matching image/route is identified. At the
relevant Texture2D application, record the RenderLeaf caller's `_drawable` and
its effective StateGraph/StateSet image, sampler unit and alpha state. Inspect
parent StateSets too; the drawable's own StateSet may not contain inherited
texture attributes. Hold the same drawable pointer across A/B in this session.
Use `RenderLeaf::render` breakpoints conditioned on that `_drawable`, then step
through its draw. Do not select the drawable merely because the GL4ES cache
claims it has the target texture: that would miss precisely the wrong-binding
case. If no RenderLeaf caller is present (upload/precompile), find the actual
render pass before attributing a draw.

Within that drawable, stop immediately at the native `glDrawElements` or
`glDrawArrays` entry, after wrapper realization. Resolve the native addresses
from the OpenGLES framework, not `gl4es_GetProcAddress`. Breakpoints must be
limited to this selected draw/thread, disabled after 1–2 draws per angle.
If the call goes through render-list replay, record its producer and replay
identity; do not equate the current RenderLeaf with deferred geometry by guess.

At the draw entry record `thread backtrace`, and, if symbols allow:

```text
expression -- glstate->texture.active
expression -- glstate->gleshard->active
expression -- glstate->bound_changed
expression -- glstate->gleshard->program
expression -- *glstate->gleshard->glprogram
expression -- glstate->enable
expression -- glstate->alphafunc
expression -- glstate->alpharef
```

For the intended sampler unit U, inspect `glstate->texture.bound[U][1]` (index
1 is ENABLED_TEX2D), its `texture`/`glname`, `actual_tex2d[U]`, and the native
program's sampler uniform. Native queries below must execute on the stopped
render thread with its original current EAGL context. Never issue queries on
an arbitrary paused main thread, and never use unqualified `glGetIntegerv`
(which could inspect a wrapper cache instead of GLES).

LLDB native-query setup (abort if any pointer is null):

```text
expression -l objc++ -- @import OpenGLES;
expression -l objc++ -- @import Darwin;
expression -l objc++ -O -- [EAGLContext currentContext]
expression -- void* $gles = (void*)dlopen("/System/Library/Frameworks/OpenGLES.framework/OpenGLES", 2)
expression -- void (*$geti)(unsigned int,int*) = (void (*)(unsigned int,int*))dlsym($gles,"glGetIntegerv")
expression -- int (*$getloc)(unsigned int,const char*) = (int (*)(unsigned int,const char*))dlsym($gles,"glGetUniformLocation")
expression -- void (*$getuniform)(unsigned int,int,int*) = (void (*)(unsigned int,int,int*))dlsym($gles,"glGetUniformiv")
expression -- void (*$active)(unsigned int) = (void (*)(unsigned int))dlsym($gles,"glActiveTexture")
expression -- int $program = 0
expression -- $geti(0x8B8D, &$program)
expression -- int $loc = $getloc($program, "diffuseMap")
expression -- int $unit = -1
```

Ensure `$program` is nonzero and `$loc >= 0`, then run:

```text
expression -- $getuniform($program, $loc, &$unit)
```
If `diffuseMap` is absent/optimized out/renamed, enumerate the program's active
uniforms using native `glGetActiveUniform` and choose the actual diffuse sampler;
do not substitute location 0. Record the unresolved names/output for follow-up
if that cannot be established. Likewise do not proceed with `$unit < 0` or
outside native GL_MAX_COMBINED_TEXTURE_IMAGE_UNITS.

For a valid sampler unit, this single expression queries the binding and
restores native active-unit selection before returning. It changes no binding:

```text
expression -- int $nativeTexture = 0
expression -- { int saved = 0; $geti(0x84E0, &saved); $active(0x84C0 + $unit); $geti(0x8069, &$nativeTexture); $active(saved); }
expression -- $program
expression -- $unit
expression -- $nativeTexture
```

Compare native texture with the logical texture object's **glname**, not its
logical **texture** number. Compare the native sampler unit with intended
OSG unit and GL4ES req_tu/act_tu. Also record native blend/depth enable and masks
if binding agrees. GLES2 alpha testing is implemented in shader code: there is
no valid native fixed-function GL_ALPHA_TEST query to settle this question.
Use shader/material alphaRef/discard and image alpha evidence instead.

If LLDB cannot resolve `dlopen`/`dlsym`, lacks symbols, or expression evaluation
fails, stop this stage and send the exact error. These commands are a proposed
device protocol, not cloud-validated LLDB execution. Do not improvise wrapper
state mutations, texture rebinding or forcing a sampler as a diagnostic fix.

Capture at most two matched draws per A/B/A angle, plus one control tree. Include
context, drawable, image path/hash, OSG texture ID/unit, GL4ES logical/native
texture IDs, cached binding, native binding, program/sampler, alpha/depth/blend
and preceding bind route. Track deletion/reupload if an ID changes meaning.
Disable the temporary breakpoints, `continue`, and turn diagnostics off after
collection. Do not reset probe budgets by editing runtime globals.

## Decision gate and validation

A corrective patch requires the same intended drawable and image to be matched
to a reproducible first divergent boundary on a bad draw. A good-angle/control
comparison must support the prediction. If native binding/sampler is correct,
move to alpha/UV/cull evidence instead of forcing a texture-cache fix. A missing
draw requires coverage/traversal proof, not inference from an exhausted log.

If LLDB cannot observe the necessary state, the next separately reviewable
instrumentation should be manually armed, exact-drawable scoped and capped to
a handful of native submissions. It must include context/lifetime, all sampled
units, intended image and native program/uniform/binding, restore any temporary
active-unit query changes, and remain off by default under PR #3. No first-
exterior auto-trigger or generic foliage-name-only filter can establish identity.

Cloud results: 159 existing host tests pass on this baseline, including WO33
blend and PR #3 disabled-path regressions. A small C compilation of the actual
GL4ES AliasExport header with `__APPLE__` and `NOEGL`, using the bundled include
directory, defines `gl4es_glBindTexture` but no `glBindTexture` symbol in `nm`.
This verifies macro behavior only, not final Mach-O routing. Pinned OSG source
was inspected directly at its exact revision. No runtime source, dependency,
shader, fog, terrain, touch, lifecycle or generated project changed. No new
regression test is needed for this documentation-only investigation. Xcode,
LLDB on iPhone, native binding parity and the causal correction remain untested
for this investigation; no renderer fix or performance claim is made.
