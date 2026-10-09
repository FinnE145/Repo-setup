## Overview
{{PROJECT_NAME}} — {{ONE_LINE_PURPOSE}}

{{OVERVIEW: two or three sentences on what it is}}

This repo runs the **lite** setup: no Plan/Implement/Verify phases, no specs, no roadmap. `.claude/flow.json` records that; `/flow update` can upgrade it to the full workflow.

## Tech Stack
{{TECH_STACK: language and exact version, framework(s), storage, environment — one bullet each}}
- Never assume an unstated version or library.

## Codebase Map
{{MAP_ENTRIES: one bullet per module, directory or file that matters, each saying what it owns}}
- Update this map when you add, move or rename something — it's what a fresh session reads first.

## Keep It Simple
- KISS. The goal is code that is **done, understandable, and works** — not production-grade or clever. AI tends to overdo complexity; don't. Reach for the simplest thing that fully solves the problem.
- **Security is the one exception to KISS — never do the bare minimum here.** Everything security-related must be done *fully and properly*, not just "right": secure coding practice (never leak tokens/secrets) **and** the implementation of things like login, auth, and session handling. Do those thoroughly.
{{HARD_REQUIREMENT: either "- The other hard requirement: never corrupt or wrongly modify <the real data/account>. Beyond security and that, favor simplicity over robustness — the rest just needs to be done right." or, with none, "- Beyond security, favor simplicity over robustness — the rest just needs to be done right."}}

## Code Hygiene
- **Comments explain *why*, not *what*** — most of the valuable ones record a failure that actually happened. Never strip them to "clean up".
- **TODOs stay rare** (aim for none), with zero `FIXME`/`HACK`/`XXX` and no commented-out code.

## Commands
{{OS_NOTE: if the repo is worked on from both Windows and macOS/Linux, add: "Commands below give a variant per OS where they differ — use the one for the OS you're running on."}}
- **Run:** {{RUN_COMMAND, or "none"}}
- **Dev port:** {{DEV_PORT, or "none"}}
- **Test:** {{TEST_COMMAND, or "none"}} — run it before telling me you're done, whenever there is one.

<!-- flow:lite-tests — keep this section only if the repo has a Test command -->
## Tests
A test's whole value is whether it can **fail**. Ask of each test what a wrong implementation would have produced, and of each module what it produces that no test reads at all. Write expected values as literals, never read back off the code under test. Never weaken or delete a test to get a green run.
<!-- /flow:lite-tests -->

## No Assumptions & the Stop-and-Ask Rule
- Never assume behavior, versions, libraries, or intent I haven't stated. If something is undefined, ask.
- **Stop-and-ask (token reduction):** the moment you're unsure or catch yourself weighing alternatives, stop right there and ask — do not keep reasoning through the options first. Ask immediately, get my answer, then continue the train of thought.
- **One try, then ask.** If an approach doesn't work on the first attempt, stop and ask for direction. Do not try a second approach, and never layer hacky fixes (overrides, workarounds) to force something through. Surface the problem instead of digging deeper.
- Prefer asking me over reading large, token-expensive docs. Only open those if I point you to them or say broader context is needed.

## When Asking Questions
- Always **number** questions (use sub-letters when nesting, e.g. 1, 2a, 2b) so I can reply item-by-item. This applies to any list I'll respond to point-by-point; plain prose replies don't need identifiers.
- **Brief first, then ballot.** Findings, reasoning and recommendations go in prose *above* the numbered list; each numbered item is the decision itself, ideally one line.
- **Compressing a question moves its "why" up, never deletes it.** If a fact matters enough to state, it stays on the page — just above the list rather than inside it.
- **Mid-run questions go through the question tool.** When you stop partway through a run for one or two questions, ask them with the question tool so I get a notification. Long question batches stay as a numbered list in chat.

<!-- flow:modules — module sections are inserted here (frontend, external constraints, deploy, …) -->

## Git Workflow
<!-- flow:git -->
Solo repo. Warn *before* acting on any of these, then do whatever I decide:
1. **No committing to `main`** unless it's a tiny fix — say so first if you're about to.
2. **Commit only when I ask**, whole files at a time, in my name only — no Claude/AI co-author or attribution line.
3. **Don't push without being asked.** Merges into `main` are `git merge --ff-only`; if it can't fast-forward, stop and flag it.
<!-- /flow:git -->
