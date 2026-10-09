# Module: python

**Applies when** the project's code is Python.

## What setup asks (skip what context already answers)
- The exact Python version (never assumed; the venv is built on it).
- Whether `venv` + `requirements.txt` is the environment (the default Finn has used), or something else.

## What it adds
- **CLAUDE.md → Tech Stack:** the Python version and environment, as stated.
- **CLAUDE.md → Commands** (give both variants when the repo is worked on from Windows and macOS/Linux):
  - Test — macOS/Linux: `venv/bin/python -m pytest` · Windows: `venv\Scripts\python -m pytest`. `-m` pins the venv interpreter rather than relying on a shim.
  - Coverage — the same with `--cov=<module>` per module touched (needs `pytest-cov`).
- **Files** (from `files/`, copied as-is):
  - `pytest.ini` — puts the repo root on `sys.path`.
  - `tests/test_conventions.py` — enforces the one-line source comment on every test. Ship it in every Python repo with tests; the phases say this convention is enforced mechanically, and this is what makes that true.
  - `tests/test_codebase_map.py` — full mode only (lite has a map but no Verify step maintaining it). Set `MODULE_DIRS` to where the repo's own modules live, and `BARE_NAME_DIRS` to any directory whose bullet in the map names files by bare name.
  - Add `pytest` (and `pytest-cov`, in full mode) to `requirements.txt`.
- **Codebase Map:** a `tests/` bullet naming `test_conventions.py` and `test_codebase_map.py` and what they enforce.
