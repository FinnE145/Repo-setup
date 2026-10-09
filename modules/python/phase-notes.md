# Python phase-notes

Read only the section for the phase you're in.

## Implement
- **Source comment format:** `# source: <spec> §<n> -- <clause>`, or the word `characterization`, **inside** the test function's body — `tests/test_conventions.py` scans function bodies, so a comment above the `def` fails it.
- **Real-data guard (any repo whose app reads data that must not be touched by tests):** `conftest.py`'s top is load-bearing and order-dependent. Redirect the data path and set dummy credentials **before the first project import** — a module that does `from config import DB_PATH` binds the path at import time, so setting the environment variable afterwards is a silent no-op and the suite runs against the real file. Then hard-check the resolved path and refuse to run if it isn't the temp one, and wrap the data-access function itself (e.g. `sqlite3.connect` *and* `sqlite3.dbapi2.connect`, which is a separate binding) so code that never consulted the configured path is caught too. Block outbound HTTP and sockets at the same point.
- **Coverage's data file is itself a SQLite database** (`.coverage`, or `.coverage.<host>.<pid>.<random>` under parallel runs). A `sqlite3.connect` guard refuses it, and `pytest --cov` then passes and exits `INTERNALERROR` on the report. Exempt it by basename (`.coverage*` only), with one test that coverage can write and one that the exemption stays that narrow.
- **Recording bugs during an audit or sweep** (not ordinary Implement work — see `lessons/testing.md`): `@pytest.mark.xfail(strict=True)` with a comment naming the findings-doc entry. `strict=True` turns the day-it's-fixed unexpected pass into a loud failure saying "remove this marker".

## Verify
- **Mutation restore, Python specifically:** Python validates a `.pyc` on `(source mtime, source size)`, so restoring a mutated file by moving a backup over it — an mtime inside the same second as the mutated write — leaves a same-size mutation (`1` -> `2`, `MAX` -> `MIN`) running from **mutated bytecode under a clean source tree**, invisible to `grep`, `git diff` and `git status`. **Restore by writing the original back, and run the child with `PYTHONDONTWRITEBYTECODE=1`.** It has already cost one session an hour of chasing a bug that did not exist.
- **Coverage:** the Coverage command with `--cov=<each module this session touched>`.
