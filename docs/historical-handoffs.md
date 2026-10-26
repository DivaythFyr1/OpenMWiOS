# Historical work-order handoffs

These seven handoffs document earlier, sequential investigations. They are
preserved verbatim at the repository root as evidence of what each run actually
proved. This index is a reading guide, not a new acceptance record. The merged
WO33 baseline and the current Draft iOS 27 lifecycle candidate are described in
[the consolidation record](consolidation-status.md) and
[the lifecycle handoff](ios27-lifecycle.md). None of the device results below
validates the current Xcode 27 scene patch.

| Handoff | Main result | Limit at that point |
|---|---|---|
| [WO13R](../WORK-ORDER-13R-HANDOFF.md) | Preserved interrupted work; compared Android shader routing and qualified the Fast build/cache path. | It did not establish a current iOS 27 launch result. |
| [WO16](../WORK-ORDER-16-HANDOFF.md) | A GL4ES guard eliminated the observed null-pointer shader-conversion crash; a device run reached engine loading/artwork and music. | Tiny viewport and later shader-link failures remained. |
| [WO17](../WORK-ORDER-17-HANDOFF.md) | Normalized the `useAdvancedShader` uniform initializer in GL4ES, resolving that compile failure. | Native `modelToClip` program-link failures followed; cross-branch cache restore was not qualified in this run. |
| [WO18](../WORK-ORDER-18-HANDOFF.md) | Identified `modelToClip` linkage across separate vertex shader units and improved PR-base cache reuse. | The diagnostic build failed before production link, so that run produced no app or device result. |
| [WO20](../WORK-ORDER-20-HANDOFF.md) | Corrected the bundled `vfs-mw` path; missing fallback GMST and dependent MWUI Lua errors disappeared. | The main menu remained visually blocked by a tiny drawable, traced to a pre-context size query. |
| [WO21](../WORK-ORDER-21-HANDOFF.md) | Reconciled drawable size after GLES context creation; the loading image grew on the device. | Presentation still froze; the 800×600 native viewport did not match the measured 1440×960 drawable. |
| [WO23](../WORK-ORDER-23-HANDOFF.md) | Prepared a fragment-library linkage correction and bounded diagnostics; local focused tests and patch application passed. | CI source validation failed on an unavailable comparison checkout before app compilation. No WO23 executable or device test resulted. |

There is no root handoff file for every intervening work order. The original
records contain exact commit IDs, run numbers, artifact hashes and caveats;
consult them before attributing a fix to a binary. Later WO33 qualification and
its unresolved issues are analyzed in [the repository audit](repository-audit.md).
