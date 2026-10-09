# Module: docker-fe-pro

**Applies when** the project is deployed to `fe-pro`, Finn's home server, as a Docker stack. Distilled from Symr's hosting step, which is the worked example.

## The machine — conventions this module relies on
**`~/SERVER.md` on `fe-pro` is authoritative over this summary.** Before writing any deploy file, read it (`ssh fe-pro cat ~/SERVER.md`, with Finn's OK) and trust it wherever it disagrees with the list below.
- Ubuntu 24.04 LTS, reached over Tailscale as `fe-pro`. Finn's user `finne` is uid:gid `1000:1000` and in the `docker` group.
- **One directory per service: `/srv/stacks/<name>/`**, holding `repo/` (the git clone), `<name>.env` (mode 600, never in git) and `data/` (bind-mounted to `/data` in the container). Creating it is the one `sudo` step; it is then `chown`ed to `1000:1000` so deploys never need `sudo`.
- A service built from source keeps its compose file in `repo/deploy/`, versioned with the code it builds — not at the stack root, where it would be a second copy free to disagree with git.
- Docker's `data-root` is on `/srv`; containers run `restart: unless-stopped`.
- **Caddy** is a machine-level stack at `/srv/stacks/caddy/` (not this repo's). It binds **only the tailnet interface** and gets Let's Encrypt certs via Cloudflare DNS-01. A service is exposed by adding a site block to its `Caddyfile` and an `A` record `<sub>.fmje.dev` → the tailnet IP (DNS-only, never proxied).
- Backups go on the OS drive under `/var/backups/<name>/`; hosted material lives on `/srv`.

## Security model — read before changing any bind
- The container publishes to **loopback only** (`127.0.0.1:<port>:<port>`), never `0.0.0.0`. A loopback publish also sidesteps Docker writing iptables rules that bypass the firewall.
- An app with no login of its own is acceptable **only because Tailscale is the boundary**. **The tripwire:** the moment the app is reachable from anything outside the tailnet — a port forward, a proxied DNS record, Caddy bound wider than the tailnet IP, `tailscale funnel`, sharing it with anyone — real authentication becomes a prerequisite, its own roadmap step, not a follow-up.

## What setup asks
- The service name (used for `/srv/stacks/<name>/`, the container and the `<name>.fmje.dev` subdomain).
- The container port, and a **health endpoint**: one that does no work and makes no outbound request (e.g. a login route that only builds a redirect), with its expected status code.
- Whether the app keeps a SQLite database worth backing up (adds the backup files), and whether the newest backup should be pulled to the laptop on deploy (and that laptop's hostname).
- Whether the server runs in-process background state (job locks, workers, singletons). If so, the production server must be **single-process** — say so in the Codebase Map.

## What it adds
- **Files** from `files/deploy/`, with the `{{…}}` values filled: `Dockerfile` (Python-shaped; adapt the base image and install step for another stack, keeping the exact-patch pin and the non-root user), `docker-compose.yml`, `app.env.example` (renamed `<name>.env.example`), `deploy.sh`, `bootstrap.md`, and — with a SQLite database — `backup.sh`, `backup.service`, `backup.timer` (renamed `<name>-backup.*`).
- **CLAUDE.md → Commands:** `Deploy: deploy/deploy.sh — run from the laptop after a branch is merged to main and pushed. One-time server setup is deploy/bootstrap.md.` On Windows, `deploy.sh` runs from Git Bash or WSL.
- **CLAUDE.md → Codebase Map:** a `deploy/` bullet, including the loopback-only rule and the tripwire above in one line each.
- **A `.gitattributes` line `*.sh text eol=lf`** — a repo checked out on Windows would otherwise give `deploy.sh` and `backup.sh` CRLF line endings, and they then fail on the server.
- **A `.dockerignore`** excluding `.git`, the venv, local data, databases and caches — so nothing local or secret is baked into the image.
- **Two copies of the data, one of them real.** Once deployed, the server's data is the source of truth and the laptop's is dev scratch; there is no laptop → server direction. Record that in CLAUDE.md's Overview.
