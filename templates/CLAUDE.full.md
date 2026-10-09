## Overview
{{PROJECT_NAME}} — {{ONE_LINE_PURPOSE}}

{{OVERVIEW: two or three sentences on what it is and the conventions it exists to serve}}

## Tech Stack
{{TECH_STACK: language and exact version, framework(s), storage, frontend approach, environment — one bullet each}}
- Fill in remaining choices as features are specced. Never assume an unstated version or library.

## Codebase Map
- `docs/` — specs and reference. Feature specs at `docs/specs/<feature>.md`; per-feature extra files (sub-specs, notes, verification reports) in `docs/<feature>/`; planning docs in `docs/Planning/`.
- **"The roadmap" always means `docs/Planning/roadmap.md`** — the standing, ordered plan of what gets built next. Each lettered step becomes its own `/flow plan` session and its own spec; landed steps stay, marked ✅ DONE and pointing at the spec that is authoritative for what actually shipped (read that spec, never the roadmap summary, before touching landed work). It also carries dated measurements that shouldn't be re-derived. Its sibling `docs/Planning/feature_ideas.md` is the loose backlog the roadmap draws from — ideas, not commitments.
- `.claude/flow.json` — which workflow mode, modules and template version this repo was set up with (`/flow update` reads it). `.claude/flow/<phase>.md`, where present, holds this repo's additions to a phase.
{{MAP_ENTRIES: one bullet per module, directory or file that matters, each saying what it owns and any invariant it keeps — what it never touches, what it alone writes}}
- (Rest TBD — update this map as directories are created.)

## Keep It Simple
- KISS. The goal is code that is **done, understandable, and works** — not production-grade or clever. AI tends to overdo complexity; don't. Reach for the simplest thing that fully solves the problem.
- **Security is the one exception to KISS — never do the bare minimum here.** Everything security-related must be done *fully and properly*, not just "right": secure coding practice (never leak tokens/secrets) **and** the implementation of things like login, auth, and session handling. Do those thoroughly.
{{HARD_REQUIREMENT: either "- The other hard requirement: never corrupt or wrongly modify <the real data/account>. Beyond security and that, favor simplicity over robustness — the rest just needs to be done right." or, with none, "- Beyond security, favor simplicity over robustness — the rest just needs to be done right."}}

## Code Hygiene
- **Comments explain *why*, not *what*** — most of the valuable ones record a failure that actually happened. Never strip them to "clean up"; a refactor should leave comment density where it was or higher.
- **Module invariants are stated, and kept.** What a module never touches, what it alone writes, what it never commits — written in the Codebase Map. Moving code between modules is exactly what violates one by accident, so check them when you do.
- **TODOs stay rare** (aim for none), with zero `FIXME`/`HACK`/`XXX` and no commented-out code.

## Commands
{{OS_NOTE: if the repo is worked on from both Windows and macOS/Linux, add: "Commands below give a variant per OS where they differ — use the one for the OS you're running on."}}
- **Run:** {{RUN_COMMAND, or "none"}}
- **Dev port:** {{DEV_PORT, or "none"}}
- **Test:** {{TEST_COMMAND, or "none yet — record it here verbatim once it exists"}}. `/flow implement` runs it before handing off and `/flow verify` gates the finish-up on it.
- **Coverage:** {{COVERAGE_COMMAND, scoped by module, or "none"}}
- Lint / format: {{LINT_COMMAND, or "none"}}
- **Deploy:** {{DEPLOY_COMMAND, or "none"}}

## Tests
The suite's whole value is whether a test can **fail**. A green test that a broken implementation would also satisfy is the most common defect there is — it turned up in every session of the test-health pass these rules come from, without exception. Two questions, always: *of each test*, what would a wrong implementation have produced here? *Of each module*, what does it produce — a stored column, a returned key, a branch — that no test reads at all? The second is not a refinement of the first, and the first cannot reach it. **Mutation is the only instrument that finds either**; coverage is structurally blind to the second, since code producing an unread value executes exactly as if it were read. `/flow implement` carries the rules for writing them and `/flow verify` for checking them.

## The Workflow: Plan → Implement → Verify
Work moves through three phases, each in its own chat, each **question-driven**. Every phase's specific rules live in the `flow` skill — invoke it at the start of the chat:
- **Plan** → `/flow plan <brain-dump>` — question-driven spec authoring; output is a committed `docs/specs/<feature>.md`.
- **Implement** → `/flow implement [spec]` — build from that spec, asking live.
- **Verify** → `/flow verify` — review the diff against the spec, run the app, finish up.

If I'm clearly in one phase but didn't invoke it, infer and load that **one** phase (never all three; if the phase is ambiguous, ask which one). The phases are self-contained — this file holds only what's true across all three.

## No Assumptions & the Stop-and-Ask Rule
- Never assume behavior, versions, libraries, or intent I haven't stated. If something is undefined, ask.
- **Stop-and-ask (token reduction):** the moment you're unsure or catch yourself weighing alternatives, stop right there and ask — do not keep reasoning through the options first. Ask immediately, get my answer, then continue the train of thought.
- **One try, then ask.** If an approach doesn't work on the first attempt, stop and ask for direction. Do not try a second approach, and never layer hacky fixes (overrides, workarounds) to force something through. Surface the problem instead of digging deeper.
- Prefer asking me over reading large, token-expensive docs. Only open those if I point you to them or say broader context is needed.

## When Asking Questions
- Always **number** questions (use sub-letters when nesting, e.g. 1, 2a, 2b) so I can reply item-by-item. This applies to any list I'll respond to point-by-point; plain prose replies don't need identifiers.
- **Brief first, then ballot.** Findings, reasoning and recommendations go in prose *above* the numbered list; each numbered item is the decision itself, ideally one line. A question carrying its own justification inline is hard to scan and hard to answer item-by-item — the identical list, re-asked with the rationale lifted out, reads far more clearly.
- **Compressing a question moves its "why" up, never deletes it.** If a fact matters enough to state, it stays on the page — just above the list rather than inside it. This is a rule about placement, not about asking less: never drop a real consideration to make a list look tidy.
- **Mid-run questions go through the question tool.** When you stop partway through a run for one or two questions, ask them with the question tool so I get a notification — I'm often away while a phase runs. Long question batches (the start of a Plan session, setup) stay as a numbered list in chat; they're too long for the tool.

<!-- flow:modules — module sections are inserted here (frontend, external constraints, deploy, …) -->

## Git Workflow
<!-- flow:git -->
Solo repo, single checkout at `{{CHECKOUT_PATH}}` (no worktrees). Branch prefixes: **`feat/`** features, **`chore/`** tooling/docs, **`fix/`** fixes. A feature branch carries both the spec (its first commit) and the implementation commits stacked on top.

These are **always-on tripwires** — warn *before* acting, then do whatever I decide. Never silently proceed past one; never refuse once I've answered.
1. **No committing to `main`.** Before any commit, check `git branch --show-current`; if it's `main` and this isn't a tiny main-level fix, stop and flag it — the work belongs on a branch.
2. **Confirm the branch before new work.** A fresh session inherits whatever branch was last checked out, which is likely wrong for new work. Confirming the branch is the *first* action of any new phase, before reading code: check `git branch --show-current`, propose a fresh branch off up-to-date `main` (or a switch to the right existing one), wait for my OK, then dive in.
3. **No premature merge/push.** Merging a branch into `main` and pushing happen only in the Verify finish-up — never during Plan or Implement.

Commits: commit only when I ask, in logical units — one for the spec, a few for implementation as needed, optionally one or more from verify. **Logical units are decided at the file level, never by splitting a single file's hunks across commits** — commit whole files together (`git add <file>`, not `git add -p`). A normal plan/implement/verify session's diff is one coherent piece of work even when a "logical" grouping would put different hunks of the same file in different commits; splitting hunks costs time, tokens, and is an easy way to stage the wrong thing. The one exception is a real mistake — edits for a genuinely separate concern that shouldn't have landed in this session/branch at all — where untangling by hunk is the correct fix, not a workflow shortcut. Commit in my name only — no Claude/AI co-author or attribution line. **Don't push without being asked.** The sanctioned merge+push is the Verify finish-up: a **`git merge --ff-only`** into `main` (keeps history linear, no merge-commit clutter) then push. This repo is solo and single-copy, so `--force-with-lease` is safe when a rewrite is the agreed fix.
<!-- /flow:git -->
