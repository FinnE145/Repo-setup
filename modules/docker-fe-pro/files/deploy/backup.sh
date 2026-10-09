#!/bin/sh
set -eu

# Runs on the HOST via a systemd timer ({{NAME}}-backup.timer + .service), not
# in the container, using the host's stdlib Python to run VACUUM INTO -- the
# sqlite3 CLI isn't needed.
#
# VACUUM INTO writes a fresh, compacted, transactionally-consistent copy while
# the app keeps running. A plain `cp` would be wrong: in WAL mode live data is
# split across the .db and its -wal, and a bare copy mid-write silently
# produces a torn file.

DB_PATH="/srv/stacks/{{NAME}}/data/{{DB_FILE}}"
BACKUP_DIR="/var/backups/{{NAME}}"
RETENTION_DAYS={{RETENTION_DAYS, e.g. 30}}

DATE="$(date -u +%Y-%m-%d)"
OUT="${BACKUP_DIR}/{{NAME}}-${DATE}.db"

mkdir -p "$BACKUP_DIR"

# sqlite3.connect() silently creates a new, empty database at a path that
# doesn't exist -- without this check a misconfigured path "succeeds" with an
# empty backup, and nobody finds out until the day it's needed.
if [ ! -f "$DB_PATH" ]; then
    echo "backup.sh: $DB_PATH does not exist" >&2
    exit 1
fi

# VACUUM INTO refuses to overwrite, so a same-day re-run would otherwise
# hard-fail against its own earlier output.
rm -f "$OUT"

python3 - "$DB_PATH" "$OUT" <<'PYEOF'
import sqlite3
import sys

db_path, out_path = sys.argv[1], sys.argv[2]
conn = sqlite3.connect(db_path)
try:
    conn.execute("VACUUM INTO ?", (out_path,))
finally:
    conn.close()
PYEOF

# Belt and braces: never prune after a failed or empty dump -- that's how you
# end up with thirty days of nothing to restore from.
if [ ! -s "$OUT" ]; then
    echo "backup.sh: $OUT was not written" >&2
    exit 1
fi

find "$BACKUP_DIR" -name '{{NAME}}-*.db' -mtime "+${RETENTION_DAYS}" -delete

echo "backup.sh: wrote $OUT"
