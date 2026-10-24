---
name: Browser-test isolation
description: Safety and runtime constraints for browser verification of this synthetic demo.
---

Keep browser regression servers separate from the development server, with
disposable synthetic storage and provider-boundary stubs plus outbound blocking.

**Why:** The workspace can have live paid-provider credentials and shared demo
profiles. Testing against the ordinary server risks charges or modifying them.

**How to apply:** Do not relax isolation to get a journey passing. When spawning
an allowlisted child process, propagate the current Python module search path:
Replit's managed packages may not be discoverable from the interpreter alone.
The unchanged frontend also depends on pinned CDN runtime scripts; allow those
scripts rather than treating all external requests as optional images/fonts.

Explicitly include the browser-test directory when passing its opt-in flag,
including in a combined backend/browser test invocation.

**Why:** The flag is registered by a nested pytest configuration; top-level
automatic discovery can reject the option before loading that configuration.

**How to apply:** Follow the documented explicit browser-directory invocation
rather than assuming the ordinary top-level command recognizes browser options.

Keep new browser and backend test basenames distinct rather than converting the
browser directory into a Python package just to avoid collection collisions.

**Why:** Both sets run under default pytest collection, and existing browser
helpers use sibling imports. A package conversion fixed one name collision but
broke those imports; unique basenames preserve both normal and opt-in collection.

**How to apply:** Verify normal collection as well as the explicit browser run
when adding browser modules; keep test organization changes narrowly scoped.
