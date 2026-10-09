# Module: protected-data

**Applies when** the project reads or writes something that must never be corrupted: a database of hand-made curation that no re-download can rebuild, a live account the code holds write access to (a music library, a calendar, a mailbox), money, or a device that can be bricked. Also when the project talks to an external API with hard limits worth writing down.

## What setup asks
- What exactly must never be corrupted or wrongly modified, in Finn's words.
- Whether one module is (or should be) the only one that writes to it.
- Any external service or API involved, and whether there's already a list of its hard limits (rate limits, things the API simply can't do, required scopes).

## What it adds
- **CLAUDE.md → Keep It Simple:** the hard-requirement line, naming the thing: "- The other hard requirement: never corrupt or wrongly modify {{THE_REAL_THING}}. Beyond security and that, favor simplicity over robustness — the rest just needs to be done right."
- **CLAUDE.md → Codebase Map:** the module that alone writes to it says so in its bullet, and every reader says it's read-only — that invariant is what a later refactor checks against.
- With an external service, a section at the `flow:modules` marker, and a stub `docs/{{service}}_constraints.md` (title plus "Hard limits of {{service}} that features must be designed around. Measured or documented facts only, each dated."):
  "## {{Service}} Constraints
  - Before proposing anything that reads or writes {{service}}, check `docs/{{service}}_constraints.md` for hard limits (what the API can't do at all, rate limits, required scopes). Don't design features the API can't support — flag the limit and ask."
