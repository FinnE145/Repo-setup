# `/flow update` — bring a repo back in line

Two jobs, in one pass: bring the repo up to the **current templates** (whatever changed in this skill since the repo last synced), and hunt for **drift** — places the repo has stopped following its own setup. It also handles mode and module changes (lite → full, adding a frontend, adding a deploy). Question-driven throughout: report, ask, change only what Finn confirms.

Runs on any model. Paths are relative to this skill's folder unless they start with the repo.

## 1. Update this skill
`git -C <this skill's folder> pull --ff-only`. If it fails, say so in one line and ask whether to continue with the installed version. Note the new commit.

## 2. Read the repo's stamp
Read `.claude/flow.json`. If it's missing, this repo was never set up — offer `/flow setup` instead. Otherwise note its `template` commit, `mode` and `modules`.

## 3. What changed in the templates
`git -C <this skill's folder> log --oneline <stamp>..HEAD -- templates modules phases lessons` and the matching `diff`. Only `templates/` and `modules/*/MODULE.md` + `files/` change what's *in the repo*; changes to `phases/`, `lessons/` and phase-notes reach the repo automatically and need no edit there — mention them in one line so Finn knows they landed.

If the stamp commit no longer exists (history rewritten), compare against the current templates directly and say so.

## 4. Hunt for drift
Check, cheaply and in this order, and keep a list:
- **CLAUDE.md vs its template:** sections missing, renamed or reordered; leftover `{{…}}` slots; `flow:` markers lost; a Commands slot that no longer matches reality (a test command that doesn't run, a port that changed). Content Finn added that isn't in the template is **his, not drift** — but note anything that looks generic enough for `/flow harvest`.
- **Codebase Map vs the real tree** (`ls` it): modules or directories missing from the map, and entries for things that are gone.
- **Full mode — the roadmap:** a *Spec index* row for every file in `docs/specs/`; every ✅ DONE step pointing at a spec that exists; the *Order* diagram and the "have landed" line agreeing with the DONE markers.
- **Full mode — specs:** recent ones missing the provenance header line or the `## Tests` section. Flag; never backfill old specs without asking.
- **Modules:** whether the module list still fits the repo (a UI appeared, a deploy was added, it became shared), and whether each module's files still match its current template.
- **Project additions** (`.claude/flow/*.md`): still accurate, and not duplicating something now in the generic phases.

## 5. Report and ask
Brief first: what changed in the templates, then the drift found, grouped. Then the decisions as one numbered list, one line each — each a proposed change Finn can say yes or no to. Recommend where you have a view; never decide.

## 6. Apply
- Confirmed changes only. Keep every `flow:` marker, and keep Finn's own content intact when restructuring around it.
- **Lite → full:** add the full template's sections around the existing CLAUDE.md content, create the roadmap and `docs/specs/`, and switch `mode`. **Full → lite** is never automatic — it would delete the roadmap and specs' role; do it only if Finn asks explicitly, and keep the files.
- Restamp `.claude/flow.json` with the new commit, mode, modules and today's date — **only once everything confirmed has been applied**, so a half-finished update never claims to be current.

## 7. Commit
Propose a `chore/flow-update` branch off up-to-date `main` before changing anything; commit only when Finn asks, whole files, in his name only. Finish-up as in Verify (ff-only merge, push) when he says so — or a pull request in a shared repo.

## 8. Point at harvest
If step 4 found anything that looked generic — a rule in this repo's CLAUDE.md or project additions that other repos would want — list it in one line each and say `/flow harvest` can carry it back into the templates.
