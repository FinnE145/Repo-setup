# Implement phase

You build the feature from its spec at `docs/specs/<feature>.md`. You are **not in a decision-making position** on code — the spec plus Finn's live answers are the source of truth, and Finn should never have to re-prompt from scratch.

## First action: check the model
Implement runs on **Sonnet** — any Sonnet version; check the family, not the version string. Check this *before anything else* — before resolving the spec, before the branch, before reading a single file. Read it straight off the environment block in your system prompt ("You are powered by the model named…"). **No command — don't shell out for this.**

If it isn't Sonnet, **stop right there**: say which model you're on and that Implement wants Sonnet, and do nothing else — no spec resolution, no branch check, no orientation, no scanning the codebase. Wait for Finn to switch models or tell you to carry on.

That block is written at session start, so it's a *fresh-session* check. If Finn has switched models mid-session it can be stale — so if he says he's already on Sonnet and the block disagrees, take his word and carry on. Never stop him twice for the same check.

## Then: load the repo's flow context
1. Read `.claude/flow.json`. If it's missing, stop: this repo hasn't been set up — offer `/flow setup`. If its `mode` is `lite`, stop and say so: this repo runs the lite setup, with no phases, specs or roadmap. Ask whether to carry on anyway or upgrade it with `/flow update`.
2. For each entry in its `modules` that has a `modules/<name>/phase-notes.md` in this skill's folder, read that file's **Implement** section, if it has one. Module notes add to this file; where they conflict, the module notes win.
3. If the repo has `.claude/flow/implement.md`, read it. Its rules add to this file's; where the two conflict, the project file wins, because it was written for this repo.
4. Any CLAUDE.md value a later step needs (a command, the dev port) that is missing or still reads `{{…}}` counts as absent — when you reach that step, name it and ask rather than guessing.

## Then resolve the spec + branch
The `/flow implement` argument, if given, names the spec (e.g. `/flow implement snapshot` → `docs/specs/snapshot.md`).
1. If an argument is given, resolve it to a spec in `docs/specs/` — exact-ish match; the branch is usually `feat/<same-ish>`.
2. If no argument, infer from the current `feat/*` branch (check `git branch --show-current`). Branch and spec slugs aren't always identical (e.g. `feat/canvas` → `docs/specs/org-canvas.md`).
3. **If exactly one spec obviously matches, use it** (even if the slug isn't 1:1). If a branch has **multiple** plausible specs (features get added to a branch over time), list the candidates and ask which — or use the argument to disambiguate.
4. Always echo what you resolved — "implementing `docs/specs/X.md` on branch `feat/Y`" — before writing any code.
5. If the expected spec/branch doesn't exist, stop and ask (the spec should already exist from the Plan phase).

Confirm you're on the right `feat/*` branch (not `main`, not an inherited wrong one) before committing anything.

## Gate: dev server must not already be running
**Skip this gate if CLAUDE.md's Commands name no dev port.**

Before editing any file, check whether something is already listening on the dev port (CLAUDE.md → Commands) — `lsof -i :<port> -sTCP:LISTEN` on macOS/Linux, `Get-NetTCPConnection -LocalPort <port> -State Listen` in PowerShell on Windows. This is a read-only check — do it before the first `Edit`/`Write` call, not after.

This isn't the same concern as CLAUDE.md's port rule (which is about *you* needing the port later, for preview/verification). This is about protecting whatever's running *right now*: a dev server with auto-reload restarts on every source save — including edits from this session, in this same single checkout — and a restart re-runs the app's startup, migrations and all, against whatever data that server points at, with zero review gate, before anything has been tested. A DB migration should never get applied to live data as a side effect of someone else's server noticing a file changed.

If the port is occupied, **stop and flag it to Finn before writing any code** — name the port, say it's likely another chat's session, and ask him to stop it. Don't work around it (different port, editing files anyway, etc.). Once he confirms it's free, proceed normally.

## While building
- **Ask live, one at a time, for anything the spec didn't decide.** The spec is meant to be complete; when a real choice surfaces mid-implementation that it didn't cover, stop and ask rather than deciding yourself. Anything you *could* have foreseen from reading the spec, ask together up front instead of trickling it.
- **One try, then ask.** If an approach fails on the first attempt, stop and ask — no second approach, no layered hacky workarounds. Surface the problem.
- Number questions (sub-letters when nesting). KISS everywhere except security and the hard requirement in CLAUDE.md's *Keep It Simple* (if it names one), which get done fully and properly.

## Writing tests
A test's whole value is whether it can **fail**. A green test that a broken implementation would also satisfy is worth no more than a tautology, and it is harder to spot because it passes and cites a real spec clause. The test-health pass these rules come from found this defect in every session it ran without exception — treat it as a new test's default state, not a rare slip.

Ask both questions. The second is not a refinement of the first, and the first cannot reach what it finds:
- **Of each test** — what would a wrong implementation have produced here? If the answer is "the same thing", the test is decoration.
- **Of each module** — what does it produce (a stored column, a returned key, a branch) that no test reads *at all*? There is no assertion there to interrogate, so the first question is blind to it.

Five shapes, each of which has shipped green at least once:
- **The fixture must disagree with every rule the implementation could fall back on**, not just the one the spec discusses. Ids that happen to sort the way the score ranks them pass against an implementation that never reads the score.
- **Where a rule spans a function and its call site, the test has to cross the seam** — testing the function alone pins the half that cannot enforce the rule by itself.
- **A status code is not an assertion.** `assert response.status_code == 200` is the cheapest un-failable route test there is; assert something that is actually *on* the page.
- **Write the expected value as a literal — never read it back off the constant, the default argument, or the query under test.** A test that derives its expectation from the thing it is testing moves with the mutant: one that both filled and asserted through a `_LOG_LIMIT` constant passed green with the constant changed, after passing review repeatedly.
- **Two fixture traps.** A falsy competitor is as blind as no competitor — `x or 0` and `x or 1` differ only when `x` is falsy, so pair a truthy row against the falsy one. And a symmetric two-item fixture lets an inverted comparison or join produce a coincidental one-for-one swap — same count, same order, different truth; add a third, unrelated item, or assert on a value rather than a count.

**Then break it.** Before handing off, change the thing each new test covers — invert the comparison, empty the returned value, drop the sort — and confirm that *exactly that test* fails. Writing a test and watching it pass proves none of the above, and mutation is the only thing that has ever caught these.

**Don't look at coverage while writing tests** — not the number, not the gap list. A coverage map in view optimises for executing lines, and the cheapest way to execute a line is a test asserting what the code already does. Verify measures; the session that writes doesn't.

Every test carries a one-line comment naming the spec clause it derives from, or `characterization` (enforced mechanically where the repo ships the convention check — the Python module does). Never obtain an expected value by running the code and then call it a specification test — that pins current behaviour, bugs included, which is the distinction the suite is built on (`lessons/testing.md` in this skill's folder has the full version, and the rest of the testing lessons; read it whenever you are writing tests).

**When a test exposes a bug:** in code this session wrote, fix the code — that is the job, and the test stays as written. In code that predates this session, stop and ask: it may be a real bug, a spec gap, or the test being wrong, and that ruling is Finn's.

## Before handing off
**Run the Test command (CLAUDE.md → Commands) before you tell Finn you're done**, whether or not you wrote tests. Breakage caught here belongs to the session that caused it; caught in Verify it belongs to a session that has to work out what happened first. If the repo has no Test command, say so plainly rather than skipping it silently.

If it's red, say so plainly with the failing test names and stop — a failure is a finding, not something to work around. Never weaken or delete a test to get a green run; if a test now asserts the wrong thing because the spec deliberately changed it, that is a change to make openly and to tell Finn about, not quietly.

## Committing
- Commit in Finn's name, only when he asks, in logical units — a few implementation commits as needed depending on scope and fixes-as-you-go, stacked on the spec commit.
- **Don't push, and don't merge to `main`** — that's the Verify finish-up, not this phase.
- **If this session started a dev server (e.g. via the preview tooling) to verify the feature, stop it once the commit lands.** Don't leave the dev port occupied for whatever session comes next — that's exactly the collision the gate above exists to prevent.
