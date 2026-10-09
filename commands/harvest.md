# `/flow harvest` — carry lessons back into the templates

The reverse of `/flow update`: find what this repo has learned that **future repos** should start with, and propose it as changes to this skill — templates, phases, modules or lessons. The changes land in this skill's own git clone and reach every device on the next `git pull`.

Question-driven: propose, ask, change only what Finn confirms. Runs on any model, but Opus judges "is this generic?" better — say so once if you're on something else, then carry on.

## 1. Update this skill, and check it's clean
`git -C <this skill's folder> pull --ff-only`, then `git status`. If the clone has uncommitted changes, stop and show them — never harvest on top of edits nobody has looked at.

## 2. Find candidates in the repo
Look where lessons get written down, cheapest first:
- **`CLAUDE.md`** — rules and paragraphs that aren't in the template it was set up from. Most are about this project; some are general rules that happened to be learned here.
- **`.claude/flow/*.md`** — this repo's additions to a phase. A rule here that doesn't mention anything project-specific is a strong candidate.
- **The roadmap** — *Cross-cutting notes*, and "Trap:" or "learned the hard way" lines in step sections.
- **Findings or post-mortem docs** under `docs/`, if Finn points you at them or their names say so. Skim their conclusions only — they are usually long, and most of their content is about this project.
- **Deviations from the templates** that look deliberate — a section reworded, a rule tightened — which may be improvements the template should take.
- **A missing module** — a kind of project (firmware, a different language, a different deploy target) this repo has worked out conventions for that no module covers.

## 3. Filter
Two tests, both required:
- **Generic.** Would it hold in a repo that shares nothing with this one but the workflow? Strip the project nouns and see whether a rule is left. If it only holds for a kind of project, it belongs in a module, not the core.
- **Worth its cost where it would live.** Every home has a price:
  - `templates/CLAUDE.*.md` — read **every turn of every chat in every repo**. The highest bar: only rules that change behaviour broadly and often.
  - `phases/*.md` — read every time that phase runs.
  - `modules/<name>/` — only in repos with that module; phase-notes only in that phase.
  - `lessons/*.md` — only when that kind of work is happening. The cheapest home for detail.

  Put each candidate in the **cheapest home that still reaches the moment it matters.**

## 4. Propose
Brief first, then one numbered item per candidate: where it comes from in this repo, the home you propose, and the **exact wording** — keep the repo's wording where it already reads well; these rules are tried and tested, and rewording them for style loses that. Say which candidates you looked at and rejected, in one line each, so Finn can overrule a rejection.

## 5. Apply and commit
- Edit this skill's clone with the confirmed changes only. A new module gets a `MODULE.md` (applies-when, what setup asks, what it adds), optional `phase-notes.md` and `files/`, and a row in `modules/README.md`.
- Commit to the clone's `main` in Finn's name only, when he asks — whole files, one commit per coherent change. **Push only when he says so**; if the push fails (no GitHub auth on this device), say so plainly and leave the commit local.
- Don't edit the repo you harvested from. Once the lesson is in the template, the repo's own copy is redundant — the next `/flow update` there will notice and ask.
- Mention which existing repos would pick the change up via `/flow update`, if Finn wants it applied there too.
