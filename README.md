# Repo-setup — the `flow` skill

Finn's project workflow for Claude Code, as one user-level skill: **Plan → Implement → Verify** phases, plus commands that set up a repo, keep it in line with the templates, and carry lessons back.

## Install (once per device)

This repository *is* the skill folder. Clone it straight into your user skills directory:

```sh
# macOS / Linux
git clone https://github.com/FinnE145/Repo-setup ~/.claude/skills/flow
```

```powershell
# Windows (PowerShell)
git clone https://github.com/FinnE145/Repo-setup $HOME\.claude\skills\flow
```

That's all. `/flow setup`, `/flow update` and `/flow harvest` run `git pull --ff-only` on this folder themselves, so every device stays current. The phases don't pull — a workflow halfway through a feature keeps the rules it started with.

## Use

| command | what it does | model |
|---|---|---|
| `/flow setup` | Sets up the repo you're in — asks what it needs, writes `CLAUDE.md` (full or lite), the roadmap and docs layout, and module files | any |
| `/flow plan <brain-dump>` | Question-driven spec authoring → a committed `docs/specs/<feature>.md` | Opus |
| `/flow implement [spec]` (or `build`) | Builds the feature from its spec, asking live | Sonnet |
| `/flow verify` | Reviews the diff against the spec, measures the tests, finishes up (ff-only merge + push) | Opus |
| `/flow update` | Brings a repo up to the current templates and hunts drift; switches mode or modules | any |
| `/flow harvest` | Finds generic lessons in a repo and proposes them as template changes here | Opus preferred |

**Full vs lite.** Full is the whole workflow. Lite is `CLAUDE.md` only — the standing preferences (questions, KISS, no assumptions, hygiene, git tripwires) with no phases, specs or roadmap. The phases stop and say so in a lite repo.

**Per-repo additions.** A repo can add rules to one phase in `.claude/flow/<phase>.md`. They're read after the generic phase and win where the two conflict. (A project-level skill named `flow` would *not* override this one — in Claude Code, personal skills beat project skills of the same name — which is why additions work this way.)

## Layout

```
SKILL.md            router — reads the argument, loads exactly one phase or command
phases/             plan.md, implement.md, verify.md
commands/           setup.md, update.md, harvest.md
templates/          CLAUDE.full.md, CLAUDE.lite.md, roadmap.md, feature_ideas.md, flow.json
modules/            per-kind-of-project additions — see modules/README.md
lessons/testing.md  testing lessons, read only when tests are being written or measured
```

## What a set-up repo carries

- `CLAUDE.md` — with `{{…}}` slots filled and `<!-- flow:… -->` markers kept (update uses them).
- `.claude/flow.json` — mode, modules, and the commit of this repo it was last synced to.
- Full mode: `docs/Planning/roadmap.md`, `docs/Planning/feature_ideas.md`, `docs/specs/`.
