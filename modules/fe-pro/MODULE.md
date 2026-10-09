# Module: fe-pro

**Applies when** the project runs on `fe-pro`, Finn's home server, or deploys to it — whether as a Docker stack (add `docker-fe-pro` too), a host service, or anything that reads the machine's own interfaces. Distilled from desk-bridge's setup.

## The rule this module exists for
**`~/SERVER.md` on `fe-pro` is the master description of the machine** — drives, the `/srv/stacks/<name>/` convention, every service and its traps. It is the single source; a repo copies from it only what is short, critical to not miss, and unlikely to change (the list below), and otherwise points at it. Anything a repo documents *about itself* (its own interface, its own quirks) lives in the repo, with a one-line pointer in `SERVER.md` — not in both.

## What setup asks
- **Where the checkout lives:** on `fe-pro`, with Claude Code sessions run on the box over SSH from the laptop (the repo's code runs where it's edited), or on the laptop (Windows, the G14), deploying to the box. This decides how a session reads `SERVER.md` and the repo's OS for every other module.
- Which parts of the machine the repo touches (a stack, a host service, system D-Bus, the AX10 LAN, …) — so the map and the section below can name them.

## What it adds
- **CLAUDE.md**, a section at the `flow:modules` marker:
  "## fe-pro
  - **`~/SERVER.md` on `fe-pro` is authoritative for the machine.** Read it before adding, moving, starting or stopping anything on the box{{, or before designing anything that touches <what this repo touches>}}. {{READ_HOW}}
  - **Anything this repo changes on the machine** — a new service, unit, stack, bind, user/group, package — **updates `SERVER.md` in the same piece of work.** Facts about this repo itself go in the repo, with at most a one-line pointer in `SERVER.md`.
  - The clock is **UTC** (the machine is in Ontario; `TZ=America/Toronto date` for local).
  - **`sudo` needs Finn's password** — anything privileged is his to run: give him the exact command.
  - **Never stop or restart another service** to free a port, memory or anything else — ask. (Minecraft in particular needs its long stop timeout or the world corrupts.)"
- `{{READ_HOW}}`, by where the checkout lives:
  - **On fe-pro:** "`.claude/settings.json` allows reading it without a prompt." — and add `"Read(//home/finne/SERVER.md)"` to `permissions.allow` in the repo's `.claude/settings.json` (create it if needed). An explicit allow rule rather than a symlink into the repo, because the permission check may follow a symlink to its target outside the repo.
  - **On the laptop:** "Read it with `ssh fe-pro cat ~/SERVER.md` — ask first." Commands in that CLAUDE.md are written for Windows (Git Bash or WSL for shell scripts).
- **CLAUDE.md → Codebase Map:** where the repo's code runs on the box, if it runs there yet.
