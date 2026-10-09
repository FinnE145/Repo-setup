# `/flow setup` — set up a repo

Sets up the repo you're in for Finn's workflow: CLAUDE.md, and in full mode the roadmap, docs layout and specs folder, plus whichever modules fit. Works on an empty folder or on an existing codebase. Everything is **question-driven** — the same rules CLAUDE.md's templates carry apply here already: never assume, number questions, brief first then ballot, one try then ask.

Runs on any model. Paths are relative to this skill's folder unless they start with the repo.

## 1. Update this skill
Run `git -C <this skill's folder> pull --ff-only`. If it fails (offline, local edits), say so in one line and ask whether to continue with the installed version — don't fix the clone yourself. Note the resulting commit (`git -C <folder> rev-parse --short HEAD`); it becomes the stamp in `.claude/flow.json`.

## 2. Find out where you are
Cheaply — list the top level, read the README and any manifest (`requirements.txt`, `pyproject.toml`, `package.json`, `platformio.ini`, `Cargo.toml`, `Dockerfile`, …), and an existing `CLAUDE.md` if there is one. Don't read the codebase in depth yet.
- **Already has `.claude/flow.json`:** stop — this repo is set up. Offer `/flow update` instead.
- **Not a git repo:** offer `git init` (with `main` as the default branch).
- **Existing `CLAUDE.md` not made by this skill:** it's Finn's — everything in it is kept unless he says otherwise. Plan to merge the template around it, and list anything that conflicts as a question.
- **Existing project-level skills** (e.g. a repo's own `plan`/`implement`/`verify` skills): leave them alone and mention them.

Also read `modules/README.md` here, to know which modules exist and when each applies.

## 3. Ask
One numbered batch, brief first. Above the list, say what you inferred from step 2 — stack, layout, whether there's a UI, whether there's a server — so Finn can confirm rather than re-type. **Skip any question the context already answers, and fold your inference into the brief instead.** Then ask whatever the selected modules' `MODULE.md` "What setup asks" sections need, in the same batch where you can foresee them. Later batches are fine ("last batch…") for things that only surface from his answers.

The core questions:
1. **Full or lite?** Full is the Plan → Implement → Verify workflow with specs, a roadmap and the finish-up rules. Lite is CLAUDE.md alone — Finn's standing preferences (asking questions, KISS, no assumptions, code hygiene, git tripwires) with no phases, specs or roadmap. Lite suits small or throwaway projects.
2. **What is it?** A name and a one-line purpose, plus a sentence or two for the Overview.
3. **Solo or shared?** Shared adds the `team` module. (Finn almost always works solo.)
4. **Stack:** language(s), framework(s), storage, and **exact versions** — never assumed.
5. **Which OS(es)** will this repo be worked on from — Windows, macOS/Linux, or both? Both means per-OS command variants.
6. **Is there a UI?** If yes: do looks matter, or function over form? (frontend module.) Decide this yourself where it's obvious — a headless bridge or a CLI has none — and say so in the brief rather than asking.
7. **Is there anything real it must never corrupt** — a database of hand-made data, a live account it holds write access to, a device — and any external API with hard limits? (protected-data module.)
8. **Dev server:** run command, port, and whether the port is fixed by something external. (dev-server module.)
9. **Tests:** the test command if it differs from the module default, or "none yet".
10. **Deploy target:** none, Docker on `fe-pro` (docker-fe-pro module, plus fe-pro), or something else — describe it. Anything that runs on or deploys to `fe-pro` at all adds the `fe-pro` module.
11. **Anything that's always true about this repo** a fresh session must know — invariants, traps, things already decided.

## 4. Propose, then wait
List, one line each: the mode, the modules, and every file you'll create or change (with the branch it'll go on — see step 6). For an existing `CLAUDE.md`, say exactly what you'll add around Finn's content. Wait for his OK.

## 5. Write
- **`CLAUDE.md`** from `templates/CLAUDE.full.md` or `templates/CLAUDE.lite.md`:
  - Fill every `{{…}}` slot from Finn's answers. A slot with no answer gets the template's stated "none" form, never an invented value. **Leave no `{{` behind** — the phases treat a leftover slot as missing and stop to ask about it.
  - Apply each module's "What it adds": sections go at the `<!-- flow:modules -->` marker; the `team` module replaces the `flow:git` block.
  - Keep the `<!-- flow:… -->` markers — `/flow update` uses them to find sections.
  - **Codebase Map:** on an existing codebase, build it from the real tree (`ls` it), one bullet per module or directory that matters, each saying what it owns — this is the first thing every later session reads. On an empty repo, leave the template's entries and the "Rest TBD" line.
  - Lite: drop the `flow:lite-tests` section if there's no test command.
- **Full mode only:**
  - `docs/Planning/roadmap.md` from `templates/roadmap.md` and `docs/Planning/feature_ideas.md` from `templates/feature_ideas.md`. If Finn has steps in mind already, add them as lettered sections in his words; otherwise leave the roadmap empty and say so.
  - `docs/specs/` (with a `.gitkeep`).
- **Module files** from each module's `files/`, filled in as its `MODULE.md` says.
- **`.claude/flow.json`** from `templates/flow.json`: the commit from step 1, the mode, the modules, today's date.

## 6. Commit
- **Empty repo:** this is the root commit, on `main` — there's nowhere else for it to go.
- **Existing repo:** propose a `chore/flow-setup` branch off up-to-date `main` before writing anything, and commit there.
- Commit only when Finn asks, whole files, in his name only — no Claude/AI attribution. Don't push. If he says finish up, `git merge --ff-only` into `main` and push (if there's a remote) — the same rules as Verify's finish-up. (In a shared repo, push the branch and offer a pull request instead.)

## 7. Hand off
Tell Finn how to start, in two or three lines:
- **Full:** the first feature is `/flow plan <brain-dump>`. If the roadmap is empty, a plan session can start by drafting its first steps with him. On an existing codebase with tests to write and no trustworthy specs, mention that `lessons/testing.md` recommends auditing specs before writing specification tests.
- **Lite:** nothing to invoke — CLAUDE.md does the work. `/flow update` can upgrade to full later.
