# Phase 1 — Branch and pull-request inventory

Audit date: 2026-10-24. See [repository-audit.md](repository-audit.md) for evidence levels, access limitations, and test results.

## Live cloud refresh — 2026-10-25

This section supersedes the historical access limitations below. All **29 upstream heads and three tags match** the audited table exactly, including recomputed B-only/H-only counts. All advertised refs were fetched successfully. There are now **22 advertised PR heads and 22 merge refs**, not 21. Git refs do not establish PR open/closed state, draft status, reviews, checks, or fork ownership. Paginated API verification remains blocked by proxy CONNECT HTTP 403 for `api.github.com`.

Upstream: `https://github.com/arjunyerevan95-dot/OpenMWiOS.git`.
Fork destination: `https://github.com/DivaythFyr1/OpenMWiOS.git`.
The destination has all 29 audited branch names and three tags; its main advanced to `3e86accde6b3bc01b9f6475ad85dbed746db21bc`, adding the four audit/roadmap documents. Upstream main remains `ed23e9c9be44893fead05c6b65f8915a6a7b53b2`. No WO39 implementation branch is advertised.

Exact dated advertisements are retained in [upstream refs](recovery/upstream-refs-2026-10-25.tsv) and [destination refs](recovery/origin-refs-2026-10-25.tsv). The tables below retain the historical audit as provenance.

### Complete live PR Git inventory

The base column is the **first parent of GitHub's advertised synthetic merge commit**, not a fresh API assertion of the current PR base branch. The merge's second parent was checked against each advertised head. Base/head repository names and current review/check status still require the API.

| PR | Head SHA | Merge-ref SHA | Merge first-parent SHA |
|---|---|---|---|
| #1 | `845183371890a789ebcacbb02e535f89248d4f39` | `70eeefc9a0bddffb745d16d47c8669939212735d` | `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` |
| #2 | `399c51d4f4ede8969f29f4d5d60cca4073a1f1fb` | `0bc1a39acc8e75d8124b68c056d75b55d877756d` | `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` |
| #3 | `0053c50296e859e65d5b30a64a39b6427ea2c9f0` | `779d396f41a35ecc2113c9ec73d679bf721f1b2e` | `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` |
| #4 | `fa7d9169be3a57d7e65f57844c799b7cee1b8505` | `955474b6b5f3fea62655216a6ae43b3ce581c041` | `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` |
| #5 | `ce7abe11a91807eff9944d6cd1c83612f43abbb0` | `f97cddcc0b82643e378055e1e09f0a51051f5b68` | `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` |
| #6 | `71227ffdafc1bc3c80688d3654b09e853913617a` | `1665ec8aa73d92afd5d82e5c4c1c0ff6c148d91c` | `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` |
| #7 | `abdc29459c1b3d7090cef45bdf49e49916099c81` | `191895a101f3dbad7feb9c34162699269be1c839` | `03d133dae7261a2004869af89f71e6eee0961c79` |
| #8 | `21ba9cd1f3ca1cc7388f506ded90275ec49953ab` | `0f2183b1f76a8132f7cbeb670e7f9c6488a77365` | `03d133dae7261a2004869af89f71e6eee0961c79` |
| #9 | `6855180e17846646f677446a84e888f1b5c896ab` | `5882f85ccb26cecca6f29327f31598f7b27eaba6` | `21ba9cd1f3ca1cc7388f506ded90275ec49953ab` |
| #10 | `41c07093a7eaa95aea6f64c84674498af23056a5` | `fdb51668132739e4fb5647bab120406873efde80` | `6855180e17846646f677446a84e888f1b5c896ab` |
| #11 | `d03d15451f8fc399cbb813c35c845754d9ce500e` | `984b239c63a1bf876672e6cee620c6100c28c08d` | `41c07093a7eaa95aea6f64c84674498af23056a5` |
| #12 | `cf1d2fd1521bc4465709a56f1a387637d474b56f` | `0fc1eb866879435cf2ecb597335bef2bf643acba` | `d03d15451f8fc399cbb813c35c845754d9ce500e` |
| #13 | `5c60db4c4f1ca5c135a0bea754496b7a2f1af3f1` | `6d8883151e28e9f6a0f68a0042973f49a2e1de61` | `cf1d2fd1521bc4465709a56f1a387637d474b56f` |
| #14 | `6db1c2af5066f810df97c5af39bdbf2a48fb86b5` | `57bdc859dedbe1e739fa24d6e9d5da8c872beaf6` | `5c60db4c4f1ca5c135a0bea754496b7a2f1af3f1` |
| #15 | `1dc819cea447f8ac40c878e1a6d7f4d478e94063` | `fcb02b6eff174ae6e04b169b5dcbb5dc3b17b89f` | `6db1c2af5066f810df97c5af39bdbf2a48fb86b5` |
| #16 | `6001b1f39dcfb94f594d3d1a80d2b801749c8a26` | `d587cc7420593c99fdb84b46e788eeb8677e69dc` | `1dc819cea447f8ac40c878e1a6d7f4d478e94063` |
| #17 | `123ae04675dda763158fa7332e8f36d64b88105d` | `42a94f8a1fa90106db27a411b461f97c95493421` | `6001b1f39dcfb94f594d3d1a80d2b801749c8a26` |
| #18 | `164abe4ba2becf46ea043811963ac28195d29bcd` | `b28161fa26800ce2377e9a75299d9a0475f829bc` | `123ae04675dda763158fa7332e8f36d64b88105d` |
| #19 | `49f5f0bd80e83ef87eaebd3f69c07072796738aa` | `5aebaf7923488753e804b4c200c07e167e67d460` | `164abe4ba2becf46ea043811963ac28195d29bcd` |
| #20 | `c82542b5daa8f70764818d0058ad47e1f541efa9` | `84fea70809a7b572dd011ac7fc7f0584a1652d9f` | `49f5f0bd80e83ef87eaebd3f69c07072796738aa` |
| #21 | `b83c65ac0f39aa6d8cadf534e14114c2fcf12b45` | `b93d6d9be3e15bf5e00df5073ff4d75b60d3fc70` | `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` |
| #22 | `5ecc3ea28bdc0bb1026acb18171339cd0825ad68` | `3230f4add79bc863fc1a37f5477a52f35659bce4` | `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` |

PR #21 is now recovered at `b83c65ac0f39aa6d8cadf534e14114c2fcf12b45`; its full object history is preserved. Its mod archive remains excluded and its payload has not been qualified.

**New PR #22:** head `5ecc3ea28bdc0bb1026acb18171339cd0825ad68`. Relative to upstream main it adds two workflow files: a generic simulator workflow and a Gradle workflow cloning `https://gitlab.com/duron27/openmw_ios.git` without a commit pin. It adds no WO33 application correction or qualification evidence. Excluded: CI and simulator work are deferred, and these workflows do not establish this port's build provenance. This addition does not change the WO33 recommendation.

## Historical inventory boundary

The non-shallow adjacent checkout contains **29 remote-tracking branch heads, three tags, and 203 reachable commits**. All cached heads were compared with the recommended baseline using their Git objects. The public PR index lists **21 open PRs, zero closed**. Direct Git/API access failed, so live-remote completeness, current review states, and inaccessible PR conversations remain unverified. This table is a recovery inventory of the available snapshot, not a claim that a fresh remote fetch succeeded.

**2026-10-25 recovery check:** all 29 cached head SHAs and three tag SHAs were compared programmatically against the tables below; no mismatches were found. A fetch of all public upstream heads, tags, PR heads, and available PR merge refs into an isolated empty repository failed DNS resolution and fetched no refs. The authenticated API requests also failed DNS resolution before receiving an HTTP response. Thus the live branch inventory and PR #21's full head SHA remain incomplete; cached agreement does not establish that upstream has not changed. See the [access recovery record](repository-audit.md#access-recovery-verification--2026-10-25).

In the table, **B-only / H-only** means commits reachable only from baseline `49f5f0b` / only from the listed head, calculated with `git rev-list --left-right --count BASELINE...HEAD`. Zero H-only means the head is already an ancestor of the baseline; it must not be cherry-picked again. `origin/HEAD` is a symbolic alias and is excluded.

| Branch | Exact head SHA | B-only / H-only |
|---|---|---:|
| `agent/bootstrap-openmw-ios` | `845183371890a789ebcacbb02e535f89248d4f39` | 108 / 0 |
| `codex/wo20-main-menu-milestone` | `21ba9cd1f3ca1cc7388f506ded90275ec49953ab` | 57 / 0 |
| `codex/wo21-post-context-drawable` | `6855180e17846646f677446a84e888f1b5c896ab` | 56 / 0 |
| `codex/wo22-presentation-fbo` | `41c07093a7eaa95aea6f64c84674498af23056a5` | 53 / 0 |
| `codex/wo23-white-world` | `d03d15451f8fc399cbb813c35c845754d9ce500e` | 49 / 0 |
| `codex/wo25a-aspect-render-scale` | `cf1d2fd1521bc4465709a56f1a387637d474b56f` | 48 / 0 |
| `codex/wo26-android-touch-controls` | `5c60db4c4f1ca5c135a0bea754496b7a2f1af3f1` | 46 / 0 |
| `codex/wo27-runtime-data-path` | `6db1c2af5066f810df97c5af39bdbf2a48fb86b5` | 45 / 0 |
| `codex/wo28-android-touch-fidelity` | `1dc819cea447f8ac40c878e1a6d7f4d478e94063` | 37 / 0 |
| `codex/wo29-ios-crash-isolation` | `6001b1f39dcfb94f594d3d1a80d2b801749c8a26` | 21 / 30 |
| `codex/wo30-renderer-touch-customization` | `470697a5fa61d68016dcf9cbe8668e778667402d` | 25 / 0 |
| `codex/wo31-exterior-renderer-correction` | `123ae04675dda763158fa7332e8f36d64b88105d` | 15 / 1 |
| `codex/wo32-targeted-renderer-boundary` | `164abe4ba2becf46ea043811963ac28195d29bcd` | 7 / 0 |
| `codex/wo33-blend-state-transition` | `49f5f0bd80e83ef87eaebd3f69c07072796738aa` | 0 / 0 |
| `codex/wo34-distance-horizon-coverage` | `c82542b5daa8f70764818d0058ad47e1f541efa9` | 0 / 2 |
| `codex/wo35-sky-blending-qualification` | `0b563307a32688a4aa5feddb6587f329f13c67b0` | 1 / 1 |
| `codex/wo36-distant-terrain-qualification` | `4f6cfc62ced645d4465f401520a1dfaca5e65ab7` | 1 / 2 |
| `codex/wo37-distant-pixel-attribution` | `7c17095ff876909e31e4c7e63702fff52b237373` | 1 / 7 |
| `codex/wo38-cold-osg-attribution` | `7dbedda156b9ab2de1b23f7119f58a6f6a0d6667` | 1 / 13 |
| `delivery/openmw-ios` | `ce7abe11a91807eff9944d6cd1c83612f43abbb0` | 90 / 0 |
| `fix/gl4es-debug-uniform-initializer` | `03d133dae7261a2004869af89f71e6eee0961c79` | 67 / 0 |
| `fix/gl4es-mainless-linked-shader` | `a6ab65a677d8c74cdf01aea982b372b9fe17f5df` | 74 / 0 |
| `fix/gl4es-modeltoclip-linkage` | `abdc29459c1b3d7090cef45bdf49e49916099c81` | 62 / 0 |
| `fix/ios-resources-bundle-collision` | `71227ffdafc1bc3c80688d3654b09e853913617a` | 85 / 0 |
| `main` | `ed23e9c9be44893fead05c6b65f8915a6a7b53b2` | 152 / 0 |
| `recovery/gate3-manifest-8451833-20260717-175347` | `399c51d4f4ede8969f29f4d5d60cca4073a1f1fb` | 106 / 0 |
| `recovery/gate4-link-0053c502-20260718` | `fa7d9169be3a57d7e65f57844c799b7cee1b8505` | 104 / 1 |
| `recovery/gate4-participation-399c51d-20260718` | `0053c50296e859e65d5b30a64a39b6427ea2c9f0` | 104 / 0 |
| `work/wo13r-android-fast-ci` | `b1faab136cf55e38a34cb10a3efa160faa7fde7a` | 75 / 0 |

## Tags

| Tag | Target SHA | Meaning |
|---|---|---|
| `delivery-run-59-artifacts` | `34a3ec1ca7af00b19edb73ada44c95de5501a37d` | Early delivery/smoke-link evidence; not the later qualified game baseline |
| `recovery-evidence-milestone2b-0053c502` | `fa7d9169be3a57d7e65f57844c799b7cee1b8505` | Scoped Gate 4 recovery; release explicitly reports a link failure |
| `ios-fast-67` | `7dbedda156b9ab2de1b23f7119f58a6f6a0d6667` | Evidence-only successor to actual build source `457ab881442302a9bd59435c1878ed4e72f6e52b` |

## Verified topology and source dispositions

The main implementation chain carries bootstrap, manifest/link recovery, delivery, resource relocation, GL4ES shader compatibility, drawable/FBO repairs, fragment linkage, aspect/render scale, touch controls, runtime data paths, and crash ownership fixes. These are inherited prerequisites, not independent PRs to merge into WO33.

```text
main → bootstrap → Gate 3 → Gate 4 participation → delivery
                                               ↘ Gate 4 link-only experiment
delivery → resource relocation → WO13R → shader repairs → WO20 → WO21
→ WO22 → WO23 → WO25A → WO26 → WO27 → WO28 → WO29 correction
→ WO30 merge dfe9e1e
   ├─ decision/evidence history → WO29 branch head 6001b1f
   └─ WO31 implementation 626b332
       ├─ final WO31 evidence 123ae04
       └─ WO32 → WO33 correction 93f892d
           ├─ final WO33 evidence 49f5f0b [recommended baseline]
           │   └─ WO34 terrain experiment c82542b
           ├─ WO35 configuration evidence 0b56330
           ├─ WO36 configuration evidence 4f6cfc6
           └─ WO37 observer 7c17095 → WO38 candidate 7dbedda
```

This graph simplifies intermediate commits but preserves the important divergence points. In particular:

- WO29's current branch name hides a documentation/decision role. All changes after `dfe9e1e` are confined to `Documentation/`, `WorkOrders/`, `Decisions/`, and `Evidence/`. Its latest WO39 activation is not a WO39 implementation. No WO39 implementation branch exists in the cached inventory; the live remote was not refreshed.
- WO30 was merged at `dfe9e1e`; do not duplicate its touch-editor changes.
- WO31's final evidence commit `123ae04` is not an ancestor of WO32/33. Its implementation through `626b332` is inherited. Preserve the additional evidence separately.
- WO33's `49f5f0b` changes only six evidence files. WO35–38 forked from its parent `93f892d`, so their stale WO33 reports do not negate the successful later qualification record.
- WO34's two unique commits introduce the terrain-radius candidate and its negative device result. Keep the evidence; exclude the implementation from consolidation.
- WO35's one and WO36's two unique commits change only evidence. They are useful falsification records, not source fixes.
- WO37/38 add an observer spanning OpenMW, OSG, GL4ES, and the app bridge. WO38 also adds cold-build recovery and a Pause candidate. Keep this line available without assuming full runtime qualification.
- The Gate 4 link branch's unique commit changes only the historical workflow, adding smoke evidence and skipping later app/package stages. Do not revive that restricted pipeline.

## Pull requests

All rows refer to the [observed upstream PR index](https://github.com/arjunyerevan95-dot/OpenMWiOS/pulls). “Mapped head” is a PR-confirmed head where available, otherwise the corresponding locally inspected implementation history; it is not a fabricated API response. Conversation pages for #1–4, #6–7, #10–11, and #13 were unavailable. Their titles were visible in the index, and their source lines were inspected locally. Draft state was directly visible for #5, #8, and #9; other current draft/review/check details are not asserted.

| PR | Indexed subject / mapped head | Audit disposition |
|---|---|---|
| [#1](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/1) | Bootstrap / `agent/bootstrap-openmw-ios` | Historical foundation already inherited |
| [#2](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/2) | Gate 3 manifest / `recovery/gate3-manifest-8451833-20260717-175347` | Manifest-resolution history inherited |
| [#3](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/3) | Gate 4 participation / `recovery/gate4-participation-399c51d-20260718` | Link-participation history inherited |
| [#4](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/4) | Gate 4 static closure / `recovery/gate4-link-0053c502-20260718` | Preserve scoped experiment; not a complete app milestone |
| [#5](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/5) | Delivery / `delivery/openmw-ios` → `main` | Buildable port history, but predates later runtime fixes; inherited |
| [#6](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/6) | Resources collision / `fix/ios-resources-bundle-collision` | Required resource relocation inherited |
| [#7](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/7) | modelToClip / `fix/gl4es-modeltoclip-linkage` | Shader linkage and cache history inherited |
| [#8](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/8) | MWUI/drawable / `codex/wo20-main-menu-milestone` | Resource mounting and drawable sizing inherited |
| [#9](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/9) | Post-context drawable / `codex/wo21-post-context-drawable` | Inherited, subsequently extended by WO22 |
| [#10](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/10) | GL4ES/SDL presentation / `codex/wo22-presentation-fbo` | Inherited presentation prerequisite |
| [#11](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/11) | Fragment linkage / `codex/wo23-white-world` | Inherited GLES shader prerequisite |
| [#12](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/12) | Aspect/render scale / `codex/wo25a-aspect-render-scale` | Inherited; reduced scale 0.58 lacks full qualification |
| [#13](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/13) | Android-derived controls / `codex/wo26-android-touch-controls` | Inherited touch foundation |
| [#14](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/14) | Runtime data path / `codex/wo27-runtime-data-path` | Inherited; current Documents path avoids persisted container UUID |
| [#15](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/15) | Touch semantics / `codex/wo28-android-touch-fidelity` | Do not use standalone: subsequent WO29 repairs a demonstrated crash |
| [#16](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/16) | Touch icon lifetime / `codex/wo29-ios-crash-isolation` | Qualified correction `45c1d8c` inherited; current head also contains later administrative history |
| [#17](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/17) | WO31 / `codex/wo31-exterior-renderer-correction` → WO29 | Diagnostics, ownership repair, incomplete sampling; not a renderer correction |
| [#18](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/18) | WO32 / `codex/wo32-targeted-renderer-boundary` → WO31 | Targeted diagnostics and routing candidate; insufficient on device without WO33 |
| [#19](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/19) | WO33 / `codex/wo33-blend-state-transition` → WO32 | Initial diagnostics evolved into qualified correction; selected baseline |
| [#20](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/20) | WO34 / `codex/wo34-distance-horizon-coverage` → WO33 | Terrain-radius hypothesis falsified for the observed symptoms; exclude code |
| [#21](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/21) | `BSlickComposer/OpenMWiOS_JumpFix:iOS_Jump_Fix` → `main`, commit prefix `b83c65a` | External data/mod workaround, not an integrated native touch patch; hold |

PR #21's [visible diff](https://github.com/arjunyerevan95-dot/OpenMWiOS/pull/21/files) adds `iosjump.zip` and instructions to load `ios_jump_unstick.omwscripts` through game configuration. The archive payload was not downloaded or inspected, and its commit object is absent locally. No device qualification is recorded in the visible conversation. Do not merge it as a proven engine fix or imply its binary payload has been audited.

## Dependency order and conflicts

The selected baseline already includes OpenMW patches **0001–0015**, GL4ES patches **0001–0009**, and the evolved OSG routing patch. Keep filename application order intact. The broad groups are:

| Layer | Required order / role |
|---|---|
| OpenMW 0001–0003 | Structural iOS port, OSG route integration, vertex transforms |
| OpenMW 0004–0009 | Relocated resources, drawable dimensions, SDL presentation, fullscreen uniform and fragment linkage |
| OpenMW 0010–0012 | Bounded white-world probes, aspect/render scale, Android-derived touch integration |
| OpenMW 0013–0015 | File diagnostics, runtime fog intent, targeted boundaries |
| GL4ES 0001–0005 | Darwin aliases, shader linking/initializers, debug boundary, external default drawable |
| GL4ES 0006–0009 | File diagnostics → observable paths → targeted boundaries → blend transitions |
| `ios/patches/osg-route-gl-entry-points-through-gl4es.patch` | Shared evolving patch: routing, target instrumentation, WO32 blend route, WO33 tracing and cache reconciliation |

WO33's final correction is not independent of that OSG patch's existing declarations and routing. Starting from the complete qualified tree is safer than reconstructing an ad hoc selection of “fix” commits.

Specific integration hazards verified by comparison:

- Baseline and the decision branch changed 19 common evidence paths after their shared ancestor. These require document-level review; overlapping paths are **not** proof of textual merge conflicts. No trial branch merge was performed.
- Baseline versus WO38 has no overlapping changed paths since `93f892d`, yet a merge would still introduce unqualified observer/Pause behavior. A conflict-free merge would not be sufficient validation.
- WO34 and WO37 use different OpenMW patch files both numbered `0016`: terrain coverage versus target-pixel presentation. A combined tree could apply both lexically; numbering does not make them mutually exclusive. Preserve the rejected terrain patch outside the baseline rather than renumbering and accidentally adopting it.
- `f3ccd53e1fa823e583057afd15e8a5ce94d0ab97` contains one build-script change, an independent build test, and WO38-specific evidence. Extract the reviewed build change with attribution if needed; copying its entire evidence payload into WO33 would misdescribe that baseline's qualification.
- `457ab881442302a9bd59435c1878ed4e72f6e52b` is a Pause candidate. Existing host fixtures pass, but final physical Pause/editor checks are not recorded. Its presence in a published IPA is not acceptance evidence.
- The local ICU triplet workaround is outside all committed upstream branches. It must not enter a recovered tree through a working-directory copy.

## Reproducing the inventory

These are read-only commands, executed against the adjacent checkout during the audit:

```sh
git for-each-ref --format='%(refname)|%(objectname)|%(symref)' refs/remotes/origin
git for-each-ref --format='%(refname)|%(objectname)' refs/tags
git rev-parse --is-shallow-repository
git rev-list --all --count
git log --all --graph --decorate --oneline
git rev-list --left-right --count 49f5f0b...HEAD_TO_COMPARE
git merge-base 49f5f0b HEAD_TO_COMPARE
git diff --name-only COMMON_ANCESTOR HEAD_TO_COMPARE
git diff 93f892d 49f5f0b -- . ':(exclude)Evidence'
```

`HEAD_TO_COMPARE` and `COMMON_ANCESTOR` are placeholders. No remote ref was rewritten or deleted. The future refresh should save exact PR head/base SHAs, including external PR refs, rather than relying only on mutable branch names or cached HTML.
