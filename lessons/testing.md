# Testing lessons

Read by Implement when it writes tests and by Verify when it measures them — never every turn. Distilled from a whole-codebase test-health pass and two mutation sweeps on Symr; each lesson below cost real time to learn. Language-specific mechanics live in the module phase-notes (e.g. `modules/python/phase-notes.md`).

## Characterization vs specification — the central distinction
- **Characterization tests**: the expected value *is* the current output, and obtaining it by running the code is correct — that is the point. They answer "did this change anything?" and nothing else. They are what make a refactor safe; they say nothing about whether current behaviour is right.
- **Specification tests**: the expected value comes from the spec. Obtaining it by running the code is a **tautology that tests nothing and silently ratifies bugs** — and it is the path of least resistance for any agent told "write tests for this", which is why it is a hard rule.
- **Every test carries a one-line source comment**: the spec clause, or `characterization`. It makes review a fast scan of (assertion, cited clause) pairs, and during a refactor it says at a glance which tests may legitimately be regenerated (function-level characterization, when a function moves) and which must never be (anything spec-derived).
- **On an existing codebase with no trustworthy specs, audit the specs before writing specification tests.** Tests written against code can only encode what it does; they freeze every existing bug into a green suite. Where code and spec differ, that difference is a decision for Finn, not something a test should quietly ratify.

## A test can be neither kind and still be green
Both kinds assume the assertion would *notice* a wrong answer. Two distinct shapes, needing two different questions:
- **The fixture is too simple** to separate two mechanisms that agree on the easy input. Bites hardest on orderings, fallbacks and which-pass-handled-this questions. Ask, of each test: *what would a broken implementation have produced here?* The discriminating case usually needs one more element, a shift, or a value the fixture builders couldn't previously express (e.g. a builder where `None` meant "use the default" could not express a real NULL — give it an explicit sentinel).
- **The observation was never made** — a column, a return value or a code path no assertion reads at all. Ask, of each *module*: *what does this produce that nothing reads?*

Coverage is blind to the second by definition, and mutation is the only thing that has found either.

## Coverage
- **A session writing tests never looks at coverage** — not the number, not the gap list. Watching the map optimises for executing lines. The rule is about *who*, not *when*: Verify measures, because it writes against a finished diff and a gap list can't bend what already got written.
- **A gap-finder, not a gate.** No numeric threshold: a suite of `assert True` reaches 100%, and a target rewards the tests worth least. Keep figures out of anything a test-writing session reads, or a bare number anchors it — upward ("beat the last one", which buys lines) or downward ("I'm probably near it, I can stop").

## Measuring
- **When a finding is "a whole category of thing is unobserved", enumerate the category — don't sample it.** Eleven sampled mutations were fixed and the write-up read as complete, while twice as many instances of the identical class sat one key over.
- **A finding fixed at the level it was found leaves the level below untouched.** Making a column observed did not make the computation behind it observed; a later sweep found the survivors there. "Is this read?" and "is this right?" are different questions.
- **A pleasing number is a prompt to check the instrument.** When measurement tooling was wrong, the symptom was usually a *better* number. Pre-flight on a green baseline, and run long batches from a frozen copy so editing the live tree can't corrupt them.
- **Probe unordered results empirically; don't reason about them.** A query with no `ORDER BY` broke ties lexically, not by insertion order — the opposite of the obvious guess. Build it, print it, then assert.
- **When a temporary safety net is doing the catching** (e.g. throwaway snapshots during a refactor), the finish line is not "the compare is clean" but "the compare is redundant" — check the permanent suite catches the same breakage before the net is deleted, because afterwards the measurement is impossible.

## Test infrastructure
- **Guard real data in layers, before anything is imported.** Redirect the data path at the very top of the test bootstrap, before any project import (an import that binds the path at import time makes a later redirect a silent no-op); then hard-check the resolved path and refuse to run the suite if it isn't the temp one; then guard the data-access function itself, so code that never consulted the configured path is caught too. Each layer catches what the others can't. Narrow, named exemptions only (e.g. the coverage tool's own data file).
- **Dummy credentials and blocked network** at the same point, which also makes it structurally impossible for a test to build a real authenticated client.
- **Nothing real committed as fixture data.** Hand-built builders make the tiny purposeful rows tests want.
- **Freeze the clock** for anything whose output depends on "now".
- **Background work runs inline or is joined before asserting**, through one shared fixture every such test uses — otherwise a leaked thread or a claimed lock surfaces as a failure somewhere unrelated.
- **Route/page tests in two layers with different lifespans.** Permanent: non-error status *plus* semantic assertions about what is on the page. Ephemeral: byte-exact golden snapshots, captured for one specific refactor and deleted after — a permanently maintained byte-exact suite fails on every feature for legitimate reasons, and **a test that routinely fails legitimately gets regenerated reflexively, at which point it protects nothing.**

## Bugs found while testing
- **Inside an Implement session, in code that session wrote:** fix the code; the test stays as written.
- **In code that predates the session:** stop and ask Finn.
- **During a dedicated audit or sweep of existing code** (where the point is to see everything before changing anything): record, don't fix. Each bug gets a test asserting the *correct* behaviour, marked as a strict expected failure citing its entry in the findings doc, so the day it's fixed the unexpected pass fails loudly. **The findings doc and the expected-failure set must match exactly.**
