---
name: Signals review and automatic refresh policy
description: User-approved boundary between unattended evidence checking, billing and scoring.
---

Newly fetched external Signals evidence must remain pending until an administrator
reviews and approves it. Automatic development checks may run best-effort every
24 hours, but must use deterministic keyword tagging, never paid models, and
must not fetch immediately on first activation or overdue restart.

**Why:** The user approved unattended source checking, not unattended billing or
unreviewed changes to career recommendations. Existing active evidence and team
V2 design must be preserved.

**How to apply:** Keep the public synthetic demo's background/manual refresh and
review mutations disabled independently of the interval setting. Never imply
that an in-process timer plus ephemeral SQLite guarantees production scheduling
or durability; that needs separately approved hosting/storage work.
