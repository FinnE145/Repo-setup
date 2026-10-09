---
name: flow
description: Finn's project workflow — Plan → Implement → Verify phases plus repo setup and maintenance. Invoke as `/flow plan <brain-dump>`, `/flow implement [spec]` (alias `build`), `/flow verify`, `/flow setup`, `/flow update`, or `/flow harvest`. Also use it whenever Finn is clearly brain-dumping a feature to spec, coding a feature from a `docs/specs/` spec, reviewing a finished feature against its spec, starting a new repo or project, or tidying how a repo is set up — even if he doesn't type the command.
---

# flow — router

This file only routes. Every real instruction lives in the one file it routes to, so a session loads **one** phase or command and never the others.

This skill's own folder (the one this `SKILL.md` is in, normally `~/.claude/skills/flow`) is a git clone of `FinnE145/Repo-setup`. Paths below are relative to it.

## Route
Read the first word of the argument:

| argument | read and follow |
|---|---|
| `plan` | `phases/plan.md` — the rest of the argument is the brain-dump |
| `implement` or `build` | `phases/implement.md` — the rest of the argument, if any, names the spec |
| `verify` | `phases/verify.md` |
| `setup` | `commands/setup.md` |
| `update` | `commands/update.md` |
| `harvest` | `commands/harvest.md` |

**No argument, or an unrecognised one:** if the repo has no `.claude/flow.json`, it hasn't been set up — offer `/flow setup`. Otherwise, if Finn is clearly in one phase, infer it and load that **one** file (never more than one; if it's ambiguous, ask which). If you inferred, say which file you loaded in one line before starting.

Read the routed file and follow it exactly as if it were this skill. Don't read the other phase or command files.
