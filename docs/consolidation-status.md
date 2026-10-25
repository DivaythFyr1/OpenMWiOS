# WO33 consolidation — 2026-10-25

Review branch: `audit/consolidate-baseline`. Do not merge automatically.

## Exact inputs and disposition

- Source baseline: `49f5f0bd80e83ef87eaebd3f69c07072796738aa`.
- Qualified source underlying that evidence: `93f892dd0cf9834259b4cad2045ddb2ef9c53ed9`.
- Fork audit documents: `3e86accde6b3bc01b9f6475ad85dbed746db21bc`.
- Original upstream main: `ed23e9c9be44893fead05c6b65f8915a6a7b53b2`.
- WO38 reference only: `7dbedda156b9ab2de1b23f7119f58a6f6a0d6667`.

A non-fast-forward merge preserves both WO33 and the fork's audit commit as ancestors. Changes relative to WO33 are README and recovery documentation only. No source cherry-picks, history rewrites, branch deletions, renderer fixes, lifecycle changes, or features. WO34 terrain, WO37/38 observer, WO38 Pause, PR #21 archive, and new PR #22 workflows are excluded. The optional WO38 GLib and local ICU build adaptations await clean Mac reproduction. Existing historical workflows remain unchanged and are not dispatched; consolidation commits carry `[skip ci]`.

## Cloud verification

- Fetched every advertised upstream head (29), tag (3), and PR head/merge ref (22 each).
- Programmatically verified every historical branch SHA and baseline divergence count, every tag, and each synthetic PR merge's second parent against the head.
- WO33 product diff against `93f892d` is empty outside Evidence.
- Bootstrap succeeded: all five pinned dependencies fetched; 15 OpenMW and nine GL4ES patches checked and applied in order.
- `PATH=/workspace/host-tools/cmake/data/bin:$PATH PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s validation -p 'test_*.py'`: **148 tests passed, no skips**, Python 3.12.14 / GCC / CMake 4.3.4 on Linux x86_64.
- Recovery bundle created and verified; see audit for path and SHA-256. This local artifact preserves all recovered project refs, including external PR history.

No full `validate-source.sh` result is asserted: its macOS tooling requirements are not satisfied on this host. No Xcode generation, iOS compilation/linking, signing, or device validation was performed.

## Local build handoff

Use a fresh Mac checkout of this review branch, not an existing edited dependency tree. Follow [integration plan step 3](integration-plan.md#step-3--define-and-verify-the-local-build-contract): select pinned CMake 4.3.4, Python 3.10+, Xcode/iPhoneOS SDK, Ninja, autotools, pkg-config and required assembler tools. Resolve the ShellCheck host architecture requirement. Run bootstrap, source validation and build-ios, then explicitly compile the generated Xcode project. Keep Personal Team and bundle ID local. The generated project is not canonical source.

The previously observed Xcode 27.1 build belongs to the local audit, not this consolidated tree. Fresh clean configure/build, link/bundle checks and Debug symbol identity remain Phase 2 gates. Physical iPhone launch/resume and renderer qualification remain separate gates. Inherited diagnostics are forced on; no performance claim is made.

## Publication and access

Git read access, push dry-run and actual creation of remote branch `audit/consolidate-baseline` succeeded for `DivaythFyr1/OpenMWiOS`, demonstrating branch write permission. `gh pr create --draft` failed with `Post https://api.github.com/graphql: Forbidden`; no PR was created. Main remains at `3e86accde6b3bc01b9f6475ad85dbed746db21bc`. The prepared PR text is retained in [recovery/pull-request.md](recovery/pull-request.md). GitHub API requests failed at proxy CONNECT with HTTP 403, including an escalated check. Authenticated identity, formal fork relationship and paginated PR states/reviews/checks remain unverified. Git ref completeness does not establish API inventory completeness.

The environment draft adds `api.github.com` while retaining presets and updates install/start instructions for the recovered source. Saving the draft does not apply or publish it. Review/save the settings and publish as required by the environment UI, then retry API verification and PR creation. Do not send secret values in chat. See the final task report for actual branch-push/PR outcome.
