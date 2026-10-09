# Modules

Setup reads this index, then only the `MODULE.md` of each module that applies. Each module has a `MODULE.md` (applies-when, what setup asks, what it adds), and optionally `phase-notes.md` (read by the phases, one section per phase, only in repos listing the module in `.claude/flow.json`) and `files/` (copied into the repo).

| module | applies when | phase-notes |
|---|---|---|
| `python` | the project's code is Python | Implement, Verify |
| `dev-server` | a local server or other port-listening process runs during development | — |
| `frontend` | there's a UI someone looks at (not a headless bridge, CLI or library) | — |
| `protected-data` | the code touches something that must never be corrupted (hand-made data, a live account it can write to, a device), or an external API with hard limits | Plan, Implement, Verify |
| `docker-fe-pro` | it deploys to `fe-pro` as a Docker stack | — |
| `team` | the repo is shared with other people | Plan, Verify |

New modules (firmware, another language, another deploy target) usually arrive through `/flow harvest`, once a repo has worked out its conventions.
