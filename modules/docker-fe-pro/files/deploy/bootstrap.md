# Bootstrap: hosting {{NAME}} on `fe-pro`

One-time setup, run by hand. Deliberately not a script: most of this is Finn's to do, and a repeatable script that silently re-did it would be dangerous. Redeploys after this go through `deploy/deploy.sh`.

**`~/SERVER.md` on `fe-pro` is authoritative** over anything assumed here — check it first, and add this service to it when done.

## 1. Point `{{NAME}}.fmje.dev` at the tailnet IP

In Cloudflare's DNS for `fmje.dev`, add an **A record** `{{NAME}}` → `fe-pro`'s tailnet IP (`SERVER.md` has it), **DNS-only** (grey cloud, not proxied). The name is public but the address is CGNAT space that only routes inside the tailnet, so anyone off it resolves the name and then can't connect — proxying it through Cloudflare's edge would trip the tripwire on the spot. Confirm from a tailnet device that `dig +short {{NAME}}.fmje.dev` returns exactly the tailnet IP.

{{EXTERNAL_REGISTRATIONS: any redirect URI, webhook or callback to register for the server's own URL — keeping the laptop's dev one}}

## 2. Create `/srv/stacks/{{NAME}}`

The one privileged step — `/srv/stacks` is root-owned. Use `ssh -t`, since `sudo` prompts.

```bash
ssh -t fe-pro "sudo mkdir -p /srv/stacks/{{NAME}} && sudo chown 1000:1000 /srv/stacks/{{NAME}}"
```

## 3. Clone the repo

```bash
ssh fe-pro "git clone {{REPO_URL}} /srv/stacks/{{NAME}}/repo"
```

## 4. Write `{{NAME}}.env`

```bash
scp deploy/{{NAME}}.env.example fe-pro:/srv/stacks/{{NAME}}/{{NAME}}.env
ssh fe-pro "chmod 600 /srv/stacks/{{NAME}}/{{NAME}}.env"
# then edit it on the server by hand -- fresh secrets, never the laptop's
```

## 5. Copy existing data across (only if there is any)

**Stop the laptop app first.** For a SQLite database, send it through `VACUUM INTO` rather than copying the file: a stopped app routinely leaves a populated `-wal` beside the `.db`, and copying only the `.db` silently drops every transaction still in it.

```bash
ssh fe-pro "mkdir -p /srv/stacks/{{NAME}}/data"
python3 -c "import sqlite3; c = sqlite3.connect('{{DB_FILE}}'); c.execute('VACUUM INTO ?', ('/tmp/{{NAME}}-transfer.db',)); c.close()"
rsync -az /tmp/{{NAME}}-transfer.db fe-pro:/srv/stacks/{{NAME}}/data/{{DB_FILE}}
rm /tmp/{{NAME}}-transfer.db
```

Check row counts match on both sides for a spread of tables before going further. Watch for stored paths that were laptop-relative — they resolve against the container's working directory, not `/data`.

## 6. Set up the backup timer (only with a database)

```bash
ssh -t fe-pro "sudo mkdir -p /var/backups/{{NAME}} && sudo chown 1000:1000 /var/backups/{{NAME}}"
ssh -t fe-pro "sudo cp /srv/stacks/{{NAME}}/repo/deploy/{{NAME}}-backup.{service,timer} /etc/systemd/system/ && \
  sudo systemctl daemon-reload && \
  sudo systemctl enable --now {{NAME}}-backup.timer"
```

Confirm with `systemctl list-timers {{NAME}}-backup.timer`.

## 7. Build and start the container

```bash
ssh fe-pro "cd /srv/stacks/{{NAME}}/repo/deploy && docker compose up -d --build"
```

## 8. Add the Caddy site block

In `/srv/stacks/caddy/Caddyfile`, add — **the `bind` line is the security boundary**; never widen it:

```caddyfile
{{NAME}}.fmje.dev {
	bind <fe-pro tailnet IP>

	tls {
		dns cloudflare {env.CF_API_TOKEN}
	}

	reverse_proxy 127.0.0.1:{{PORT}}
}
```

Then `ssh fe-pro "cd /srv/stacks/caddy && docker compose restart caddy"`. Confirm `ss -ltn` on the box shows `:443` bound to the tailnet IP — **not** `0.0.0.0` or `*`.

## 9. Verify

From a tailnet device, browse to `https://{{NAME}}.fmje.dev/` and confirm it loads with a Let's Encrypt certificate (a `curl: (60)` means the DNS-01 challenge hasn't completed — `docker logs caddy`). {{APP_CHECKS: what to look at in the app to know the data and auth came across}}

Finally, add the service to `~/SERVER.md` on `fe-pro`.
