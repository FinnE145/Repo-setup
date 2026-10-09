"""CLAUDE.md's Codebase Map, checked against the tree.

**Deliberately narrow: a list against a list, with no numbers parsed out of
prose.** A check of the map's numeric claims ("three hooks", "four jobs")
would catch real drift, but it greps English that gets rewritten constantly --
rephrase "three hooks" as "a trio of hooks" and it fails legitimately, which is
precisely the shape of test that gets regenerated reflexively until it
protects nothing.

What is left cannot fail for a rewording, and catches the drift class that
matters most -- **a module added and never documented** -- plus its mirror, a
module the map still names after it is gone.

Scope: the modules under MODULE_DIRS (one bullet each in the map). It does
*not* cover `tests/` -- demanding every test file appear in the map would fail
legitimately the first time anyone adds one.
"""

import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
MAP = os.path.join(ROOT, "CLAUDE.md")

#: Where the repo's own modules live, relative to the root. "." means
#: root-level files only; any other entry is walked recursively. Setup fills
#: this in; update it when the layout changes.
MODULE_DIRS = ["."]

#: Directories a bare file name in the map may be resolved against (the map
#: names files by path, or by bare name inside the bullet for their directory).
BARE_NAME_DIRS = ["tests", "scripts"]

#: Any `foo.py` or `dir/foo.py` inside backticks. The map writes every file
#: reference that way, and restricting to backticks keeps ordinary prose about
#: "the app.py routes" from being read as a path.
_PY_IN_BACKTICKS = re.compile(r"`([A-Za-z0-9_./-]+\.py)`")


def named_py_files(text):
    return sorted(set(_PY_IN_BACKTICKS.findall(text)))


def repo_modules(root=ROOT, module_dirs=MODULE_DIRS):
    out = []
    for d in module_dirs:
        base = os.path.join(root, d)
        if d == ".":
            out += [f for f in os.listdir(base) if f.endswith(".py")]
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if x != "__pycache__"]
            out += [os.path.relpath(os.path.join(dirpath, f), root).replace(os.sep, "/")
                    for f in filenames if f.endswith(".py")]
    return sorted(out)


def missing_from_map(text, modules):
    return [m for m in modules
            if f"`{m}`" not in text and f"`{os.path.basename(m)}`" not in text]


def named_but_gone(text, root=ROOT):
    def exists(named):
        candidates = [named] + [os.path.join(d, named) for d in BARE_NAME_DIRS]
        return any(os.path.exists(os.path.join(root, c)) for c in candidates)
    return [n for n in named_py_files(text) if not exists(n)]


def _map_text():
    with open(MAP, encoding="utf-8") as fh:
        return fh.read()


def test_every_module_in_the_repo_appears_in_the_codebase_map():
    # source: CLAUDE.md Codebase Map -- the map must cover the real tree;
    # Verify's finish-up updates it, and this holds that in place.
    missing = missing_from_map(_map_text(), repo_modules())
    assert missing == [], f"modules absent from CLAUDE.md's codebase map: {missing}"


def test_every_module_the_codebase_map_names_exists():
    # source: CLAUDE.md Codebase Map -- the reverse half: a map entry
    # outliving its module is drift too.
    gone = named_but_gone(_map_text())
    assert gone == [], f"CLAUDE.md names files that do not exist: {gone}"


def test_the_map_checks_can_actually_fail(tmp_path):
    # source: flow lessons/testing.md -- a scan asserting an empty list is the
    # shape likeliest to stop testing anything, so both halves are checked
    # against a synthetic tree whose answers are known. Synthetic on purpose:
    # it must hold on a brand-new repo with nothing to map yet.
    (tmp_path / "app.py").write_text("")
    (tmp_path / "pkg" / "sub").mkdir(parents=True)
    (tmp_path / "pkg" / "sub" / "deep.py").write_text("")
    modules = repo_modules(str(tmp_path), [".", "pkg"])
    # The recursive walk must actually descend.
    assert modules == ["app.py", "pkg/sub/deep.py"]
    text = "- `app.py` -- the app\n- `ghost.py` -- deleted long ago\n"
    assert missing_from_map(text, modules) == ["pkg/sub/deep.py"]
    assert named_but_gone(text, str(tmp_path)) == ["ghost.py"]
