"""The suite's own conventions, made mechanical.

Every test carries a one-line source comment naming where its expected value
came from: the spec clause it derives from, or the word `characterization`
where the expected value *is* the current behaviour. It is not decoration --
it makes review a scan of (assertion, cited clause) pairs, and during a
refactor it says at a glance which tests may legitimately be regenerated and
which must never be. A convention that is only checked by eye drifts: on the
project this came from, a consolidated pass found 32 tests with no source
line at all. A test can hold it in place for free, so one does.
"""

import ast
import pathlib

#: What a source line may cite: `# source: <spec> §<n> -- <clause>`, or the
#: literal word `characterization`. It goes *inside* the function body.
SOURCE_MARKERS = ("# source:", "characterization")

TESTS_DIR = pathlib.Path(__file__).parent


def _test_functions(root=TESTS_DIR):
    """Every `def test_*` under `root`, with its file, line and body text."""
    for path in sorted(root.rglob("test_*.py")):
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                body = "\n".join(lines[node.lineno - 1: node.end_lineno])
                yield path.name, node.lineno, node.name, body


def missing_source(functions):
    return [
        f"{name}:{line} {func}"
        for name, line, func, body in functions
        if not any(marker in body for marker in SOURCE_MARKERS)
    ]


def test_every_test_declares_where_its_expected_value_came_from():
    # source: flow lessons/testing.md -- "Every test carries a one-line source
    # comment: the spec clause, or `characterization`."
    missing = missing_source(_test_functions())
    assert missing == [], (
        f"{len(missing)} test(s) with no source comment. Add a one-line "
        "`# source: <spec> §<n> -- <clause>` inside the test naming what the "
        "expected value derives from, or the word `characterization` where "
        "the expected value *is* the current behaviour:\n  " + "\n  ".join(missing)
    )


def test_the_source_convention_check_can_actually_fail(tmp_path):
    # source: flow lessons/testing.md -- a whole-suite scan asserting an empty
    # list is the shape likeliest to silently stop testing anything (a glob
    # that matches nothing, a walk that finds no functions), so this pins that
    # the scan sees real tests and that a bare test is genuinely detected.
    # Synthetic on purpose: it must hold on a brand-new repo with no other tests.
    (tmp_path / "test_fake.py").write_text(
        "def test_bare():\n    assert True\n\n"
        "def test_cited():\n    # source: spec §1 -- a clause\n    assert True\n",
        encoding="utf-8",
    )
    found = list(_test_functions(tmp_path))
    assert [f for _, _, f, _ in found] == ["test_bare", "test_cited"]
    assert missing_source(found) == ["test_fake.py:1 test_bare"]
    # And the scan of the real suite sees at least this file's own tests.
    assert any(f == "test_every_test_declares_where_its_expected_value_came_from"
               for _, _, f, _ in _test_functions())
