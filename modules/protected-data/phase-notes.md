# protected-data phase-notes

Read only the section for the phase you're in. "The real thing" is whatever CLAUDE.md's hard requirement names.

## Plan
- A feature that writes to the real thing gets its write path named in the spec — which module does it, and what it must never do — and its Tests section names the invariant to assert, not just the happy path.

## Implement
- Before the first test that could reach the real thing runs, the suite must already be guarded against it in layers (redirect before any import, hard-check the resolved target and refuse to run otherwise, guard the access function itself, dummy credentials, blocked network). `lessons/testing.md` has the reasoning; the language module's phase-notes have the mechanics. If the guard doesn't exist yet, building it comes first and is not KISS territory.
- Never run anything that writes — a script, a migration, a one-off — against the real thing to "check it works". Ask.

## Verify
- Confirm nothing in this session's diff writes to the real thing outside the module that owns that write, and that the dev run you did used dev data, not the real copy.
