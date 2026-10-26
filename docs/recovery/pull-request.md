> Archived PR #1 proposal. It was merged into `main` at
> `31db72918ece9003e3be9bfc410029546a846f1a`. For the current lifecycle
> candidate, see [ios27-lifecycle.md](../ios27-lifecycle.md).

Restore the complete WO33 source baseline at 49f5f0bd80e83ef87eaebd3f69c07072796738aa to the fork's documentation-only main through a history-preserving review branch. Merge the existing audit commit 3e86accde6b3bc01b9f6475ad85dbed746db21bc, update the live inventory and document build handoff and limitations. Runtime code and patch stack are unchanged from WO33.

Fetched 29 upstream branches, three tags and all 22 advertised PR heads/merge refs. Audited branch/tag SHAs remain unchanged. New PR #22 adds deferred workflows, including an unpinned different source repository; excluded from this baseline. Preserve WO38 and other unmerged history in existing fork branches plus a verified local recovery bundle. No branches are deleted or rewritten.

Validation: bootstrap succeeded with pinned sources and all 15 OpenMW/nine GL4ES patches; 148 existing host tests passed without skips using Python 3.12.14, GCC and CMake 4.3.4. Shell syntax, whitespace, product-tree identity and ancestry checks passed. No Xcode build or physical device validation is claimed. No optional GLib/ICU adaptation, renderer/lifecycle fix or new feature is included.

API connectivity and paginated PR/review metadata require rechecking: cloud API requests encountered proxy CONNECT 403. Mac configure/build/link and iPhone runtime gates remain outstanding. Keep this PR in draft and do not merge automatically. CI remains deferred; commits use [skip ci].
