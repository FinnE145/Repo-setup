#!/bin/sh
set -eu

# Run from the laptop, after the branch has been merged to main and pushed --
# that's the Verify finish-up's job, not this script's. On Windows, run it
# from Git Bash or WSL.

HOST="fe-pro"
NAME="{{NAME}}"
REPO="/srv/stacks/$NAME/repo"
COMPOSE="$REPO/deploy/docker-compose.yml"
HEALTH_URL="http://127.0.0.1:{{PORT}}{{HEALTH_PATH}}"
HEALTH_CODE="{{HEALTH_CODE}}"

echo "deploy.sh: pulling latest on $HOST"
ssh "$HOST" "git -C '$REPO' pull --ff-only"

echo "deploy.sh: rebuilding and restarting the container"
ssh "$HOST" "docker compose -f '$COMPOSE' up -d --build"

echo "deploy.sh: waiting for the health check"
# `up -d` returns as soon as the container is *created*, not when the server
# is listening, so this retries for up to 30s. The health target must do no
# work and make no outbound request -- a health check that spent an API call
# or triggered a recompute every time would be worse than none. Run over ssh:
# the port is published to fe-pro's own loopback only.
healthy=0
i=1
while [ "$i" -le 30 ]; do
    code="$(ssh "$HOST" "curl -s -o /dev/null -w '%{http_code}' $HEALTH_URL" 2>/dev/null || true)"
    if [ "$code" = "$HEALTH_CODE" ]; then
        healthy=1
        break
    fi
    sleep 1
    i=$((i + 1))
done

if [ "$healthy" != "1" ]; then
    echo "deploy.sh: health check failed -- $HEALTH_URL did not return $HEALTH_CODE within 30s" >&2
    exit 1
fi

echo "deploy.sh: healthy"

# --- Optional: pull the newest backup down to the laptop -------------------
# Delete this block if the app has no backups. Gated on one specific laptop so
# an agent on another machine doesn't quietly drag the data down. A
# mistake-catcher, not a security control: `scutil` is macOS-only, so the
# check fails closed on Linux and Windows.
LAPTOP="{{LAPTOP_HOSTNAME}}"
if [ "$(scutil --get LocalHostName 2>/dev/null || true)" != "$LAPTOP" ]; then
    echo "deploy.sh: not $LAPTOP, skipping the backup pull"
    exit 0
fi

# Failure past this point never fails the deploy -- it already succeeded
# above. Print a clear warning and exit 0; the copy is a bonus.
set +e
DEST="$HOME/{{NAME}}-backups"
mkdir -p "$DEST" || { echo "deploy.sh: could not create $DEST, skipping the backup pull" >&2; exit 0; }

latest="$(ssh "$HOST" "ls -t /var/backups/$NAME/$NAME-*.db 2>/dev/null | head -1" 2>/dev/null)"
if [ -z "$latest" ]; then
    echo "deploy.sh: no backup found on $HOST yet, skipping the pull"
    exit 0
fi

echo "deploy.sh: pulling $latest down to $DEST/"
rsync -az "$HOST:$latest" "$DEST/" || { echo "deploy.sh: backup pull failed -- deploy already succeeded" >&2; exit 0; }

echo "deploy.sh: done"
exit 0
