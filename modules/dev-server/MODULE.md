# Module: dev-server

**Applies when** the project runs a local server (or other long-lived process listening on a port) during development.

## What setup asks
- The run command, and the port.
- Whether the port is **fixed** — something external is registered against it (an OAuth redirect URI, a webhook, a device that connects to it) — or merely conventional.
- Whether the dev server auto-reloads on file saves. (If it does, Implement's port gate is protecting live data from a reload; if it doesn't, the gate still stops two sessions fighting over one port.)

## What it adds
- **CLAUDE.md → Commands:** `Run:` and `Dev port:` filled in. The phases key off `Dev port:` — Implement's gate and the stop-your-server rules only apply when it names a port.
- **CLAUDE.md → Commands**, directly under `Dev port:`, one of these two bullets:
  - Fixed port: "- **Port {{DEV_PORT}} is not negotiable for the dev loop** — {{WHY, e.g. the OAuth redirect URI `http://127.0.0.1:{{DEV_PORT}}/callback` is registered against it, so the dev app can't authenticate on any other port}}. If it's occupied (usually another chat's server) or the app is otherwise unreachable, **stop and ask me to free it**. Don't reassign the port, don't fall back to the test client or a headless workaround, and don't skip the verification."
  - Conventional port: "- If the dev port is occupied, it's usually another chat's server — **stop and ask me to free it** rather than picking another port or skipping the verification."
- If Finn uses Claude Code's preview tooling for this repo, offer to register the run command in `.claude/launch.json` so a session can start the server through it rather than a raw shell command. Ask; don't assume.
