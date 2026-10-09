# Module: team

**Applies when** the repo is shared with other people. Finn almost always works solo, so this exists mainly as a guard: the solo rules (ff-only merges into `main` yourself, force-pushing a rewrite, one checkout) range from rude to destructive on a shared repo.

## What it changes
- **CLAUDE.md → Git Workflow:** replace everything between `<!-- flow:git -->` and `<!-- /flow:git -->` with:

  "Shared repo — other people push here. Branch prefixes: **`feat/`** features, **`chore/`** tooling/docs, **`fix/`** fixes.

  These are **always-on tripwires** — warn *before* acting, then do whatever I decide. Never silently proceed past one; never refuse once I've answered.
  1. **Never commit to `main`, and never merge into it yourself.** Work lands through a pull request that someone reviews.
  2. **Confirm the branch before new work**, and fetch first — `main` moves without us here. Cut new branches from an up-to-date `origin/main`.
  3. **Never rewrite pushed history** — no `--force`, no `--force-with-lease`, no rebasing a branch someone else may have pulled.

  Commits: commit only when I ask, whole files at a time, in my name only — no Claude/AI co-author or attribution line. Don't push without being asked."
- **flow.json:** `team` in `modules`.
