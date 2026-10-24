---
name: Integrity baseline policy
description: Why original design preservation must be separated from intentional release evolution.
---

Preserve the historical original manifest; accept intentional source/data evolution
only through individually reviewed, documented hashes, never blanket exclusions.

**Why:** The upstream release itself had integrity mismatches from catalogue,
provider and scoring evolution. Restoring those files to the original hashes
would discard intended product behavior, not repair Replit setup damage.

**How to apply:** Consult the integrity review before changing hash policy.
Keep original design assets protected and distinguish byte preservation from
behavioral correctness. Do not imply a hash check covers unlisted modular files.

Editable post-import modules and hand-maintained course additions should use
explicit coverage contracts rather than blanket new hashes. Retained legacy
fragments are not certified immutable originals merely because they are unused.

**Why:** Freezing evolving implementation bytes would obstruct intended UI/data
updates; an inventory and independent assembly contract detect accidental loss
without silently blessing a changed generated page.

**How to apply:** Classify new files in covered scopes deliberately, review recipe
changes independently of rebuilt output, and retain the separate reviewed-hash
approval requirement for the assembled page.
