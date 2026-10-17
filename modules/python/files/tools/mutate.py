#!/usr/bin/env python3
"""Mutation checks: break the code one small way at a time and see whether the tests notice.

    .venv/bin/python tools/mutate.py SPEC.py [-j 4] [--timeout 120] [--root DIR]

SPEC.py defines `MUTATIONS = [(file, old, new, [pytest args]), ...]`: in `file` (relative to the root),
`old` must occur exactly once and is replaced by `new`; the pytest arguments name the tests that should fail.
A mutation is **killed** when pytest fails or times out, and **SURVIVED** when it passes (a test that can't
fail), or **SKIP** when `old` is not found exactly once (the spec is out of date).

Each worker has its own copy of the root, so mutations run in parallel without touching the real tree, and
the copy is restored by writing the original text back (never by moving a backup: a same-size mutation
restored within the same second would otherwise run from stale bytecode) with bytecode writing off.
A mutation that hangs a test is stopped after --timeout seconds instead of stalling the run. Exit status 1
if anything survived or was skipped.
"""
import argparse
import os
import queue
import runpy
import shutil
import signal
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
#: Not copied: history, caches, and the venv (the copies use the caller's interpreter).
IGNORE = shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache", ".coverage*")


def run_pytest(work, args, timeout):
    """True if pytest failed (or hung and was stopped), False if it passed."""
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    proc = subprocess.Popen([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *args],
                            cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            start_new_session=True)
    try:
        proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        # TERM first so fixtures can remove what they started (a broker container); then KILL.
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            proc.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.communicate()
        return True
    return proc.returncode != 0


def try_mutation(work, mutation, timeout):
    path, old, new, args = mutation
    target = Path(work) / path
    original = target.read_text()
    if original.count(old) != 1:
        return "SKIP", f"found {original.count(old)}x"
    try:
        target.write_text(original.replace(old, new))
        return ("killed" if run_pytest(work, args, timeout) else "SURVIVED"), ""
    finally:
        target.write_text(original)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run a spec of mutations against the tests.")
    parser.add_argument("spec")
    parser.add_argument("-j", "--jobs", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)
    mutations = runpy.run_path(args.spec)["MUTATIONS"]
    jobs = max(1, min(args.jobs, len(mutations)))
    base = Path(tempfile.mkdtemp(prefix="mutate-"))
    free = queue.Queue()
    try:
        for i in range(jobs):
            copy = base / f"w{i}"
            shutil.copytree(args.root, copy, ignore=IGNORE)
            free.put(copy)

        def work_on(mutation):
            copy = free.get()
            try:
                status, note = try_mutation(copy, mutation, args.timeout)
            finally:
                free.put(copy)
            print(f"{status}: {mutation[0]}: {mutation[1][:50]!r} -> {mutation[2][:40]!r} {note}", flush=True)
            return status

        with ThreadPoolExecutor(jobs) as pool:
            results = list(pool.map(work_on, mutations))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    bad = [r for r in results if r != "killed"]
    print(f"{len(results) - len(bad)} killed, {len(bad)} survived or skipped")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
