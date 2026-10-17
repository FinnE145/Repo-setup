# Module: two-checkouts

**Applies when** a solo repo is worked on from two checkouts on different machines, each owning part of the tree (e.g. the server code on `fe-pro`, the firmware on the laptop the board is plugged into), with work moving between them only through GitHub. Not for worktrees on one machine, and not with `team` (ask Finn how to combine the two if both ever apply). Distilled from desk-bridge (since roadmap E, 2026-10-13).

## What setup asks
- Both checkouts: machine and path, and which folders each one owns.
- Which phases run where (usually: Plan on either, Implement and Verify where the code is built and tested).

## What it adds
- **CLAUDE.md → Git Workflow**, inside the `flow:git` block:
  - The first paragraph's opening becomes: "Solo repo, two checkouts (no worktrees): `{{MAIN_CHECKOUT}}` on {{MAIN_MACHINE}} for everything but {{OTHER_FOLDERS}}, and `{{OTHER_CHECKOUT}}` on {{OTHER_MACHINE}} for {{OTHER_FOLDERS}}. Work moves between them only through GitHub: **pull the branch before starting a phase**." The branch-prefix sentence and the rest stay.
  - Tripwire 3 gains: "**The one exception: a step implemented on {{OTHER_MACHINE}} pushes its feature branch at the end of Plan** (asking first, the same way Verify does), so the other machine can pull it; later pushes of that branch happen when I say. Merging into `main` stays Verify's."
  - The closing sentence becomes: "This repo is solo, so `--force-with-lease` is safe when a rewrite is the agreed fix, but only for a branch the other checkout hasn't pulled; if it has, ask first."
- **The other checkout's folder gets its own `CLAUDE.md`** (`{{OTHER_FOLDERS}}/CLAUDE.md`; the `firmware` module writes it when that's the folder). It says the root `CLAUDE.md` applies there too, names the root sections that don't (the main machine's *Commands*, its machine module's section), carries that machine's own commands, and ends with:
  "## Git
  This checkout shares the repo with {{MAIN_MACHINE}}'s (root `CLAUDE.md`, *Git Workflow*):
  - pull the branch before starting a phase;
  - a step's branch is pushed at the end of Plan, after asking;
  - push again only when I say, so the other machine can pull."
- **Root `CLAUDE.md`:** the sections that hold only on the main machine say so in one line (e.g. "On {{OTHER_MACHINE}} this section and *Commands* don't apply: …").
