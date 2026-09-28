#!/usr/bin/env python3
"""Fail if the public checkout crosses the current student-solution boundary."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_DIRS = {"_instructor", "instructor", "solutions", "answer_keys"}
FORBIDDEN_FILE_MARKERS = (
    "_solution",
    "-solution",
    "solution_",
    "_answer_key",
    "-answer-key",
    "worksheet_sol",
)
TICTACTOE_FUNCTIONS = (
    "player",
    "actions",
    "result",
    "winner",
    "terminal",
    "utility",
    "minimax",
)

MASTERMIND_EXERCISE = "Mastermind/mastermind_exercise.py"
MASTERMIND_TODOS = 6
MASTERMIND_LEAKED_SYMBOLS = ("yellow2", "green3")

# Functions that must still be clean starter stubs in the public checkout.
STARTER_STUBS: dict[str, tuple[str, ...]] = {
    "Search/degrees.py": ("shortest_path",),
    "tic-tac-toe/tictactoe.py": TICTACTOE_FUNCTIONS,
}

# Functions whose worked solution has been released after the deadline.
# Moving a name here is the deliberate act of publishing that answer.
RELEASED_SOLUTIONS: dict[str, tuple[str, ...]] = {
    "Search/degrees.py": ("shortest_path",),
    "tic-tac-toe/tictactoe.py": TICTACTOE_FUNCTIONS,
}


def public_files() -> list[Path]:
    """Return tracked files, or all candidate files before the first commit."""
    try:
        output = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        output = b""

    if output:
        return list(dict.fromkeys(ROOT / item.decode() for item in output.split(b"\0") if item))

    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(ROOT).parts
    ]


def check_paths(files: list[Path]) -> None:
    for path in files:
        relative = path.relative_to(ROOT)
        lowered_parts = {part.lower() for part in relative.parts}
        lowered_name = relative.name.lower()
        assert not (lowered_parts & FORBIDDEN_DIRS), (
            f"instructor-only directory is public: {relative}"
        )
        assert not any(marker in lowered_name for marker in FORBIDDEN_FILE_MARKERS), (
            f"answer-bearing filename is public: {relative}"
        )
        assert path.suffix not in {".pyc", ".pyo"}, (
            f"generated Python bytecode is public: {relative}"
        )


def functions(path: Path) -> dict[str, ast.FunctionDef]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def is_clean_stub(function: ast.FunctionDef) -> bool:
    body = list(function.body)
    if body and isinstance(body[0], ast.Expr):
        value = body[0].value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            body.pop(0)
    if len(body) != 1 or not isinstance(body[0], ast.Raise):
        return False
    exception = body[0].exc
    return isinstance(exception, ast.Name) and exception.id == "NotImplementedError"


def check_python_boundaries() -> None:
    for relative, names in STARTER_STUBS.items():
        path = ROOT / relative
        if not path.exists():
            continue
        defined = functions(path)
        for name in names:
            if name in RELEASED_SOLUTIONS.get(relative, ()):
                continue
            assert name in defined, f"{relative}: {name}() is missing"
            assert is_clean_stub(defined[name]), (
                f"{relative}: {name}() must remain a clean starter stub"
            )

    for relative, names in RELEASED_SOLUTIONS.items():
        path = ROOT / relative
        assert path.exists(), f"released solution file is missing: {relative}"
        defined = functions(path)
        for name in names:
            assert name in defined, f"{relative}: released {name}() is missing"
            assert not is_clean_stub(defined[name]), (
                f"{relative}: {name}() is listed as released but is still a stub"
            )


def check_mastermind_boundary() -> None:
    path = ROOT / MASTERMIND_EXERCISE
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    todos = sum(1 for line in text.splitlines() if line.startswith("# TODO "))
    assert todos == MASTERMIND_TODOS, (
        f"{MASTERMIND_EXERCISE}: expected {MASTERMIND_TODOS} TODO blocks, found {todos}"
    )

    for symbol in MASTERMIND_LEAKED_SYMBOLS:
        assert symbol not in text, (
            f"{MASTERMIND_EXERCISE}: leaks the answer symbol {symbol}"
        )

    tree = ast.parse(text, filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if "knowledge" not in {t.id for t in node.targets if isinstance(t, ast.Name)}:
            continue
        call = node.value
        assert (
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id == "And"
            and not call.args
        ), f"{MASTERMIND_EXERCISE}: the knowledge base must start out empty"


def check_learning_boundary() -> None:
    folder = ROOT / "Counterfeit banknotes with scikit learn"
    if not folder.exists():
        return
    names = {"README.md", "banknotes.csv", "Learning_exercise.ipynb",
             "learning_by_hand.py", "week6_tuesday_code_card.pdf"}
    assert {p.name for p in folder.iterdir() if p.is_file()} == names, "Week 6 file allowlist differs"
    data = folder / "banknotes.csv"
    assert hashlib.sha256(data.read_bytes()).hexdigest() == "71f403bf5a743b8bb4658cae2fb8b82e98a3d79a886facc56a77038b5c5d801d", "Banknotes data changed"
    with data.open(newline="") as stream:
        rows = list(csv.reader(stream))
    assert rows[0] == ["variance", "skewness", "curtosis", "entropy", "class"]
    assert len(rows) == 1373 and all(len(row) == 5 for row in rows)
    assert sum(int(row[4]) for row in rows[1:]) == 610
    for row in rows[1:]:
        assert int(row[4]) in (0, 1)
        for value in row[:4]:
            float(value)
    notebook = json.loads((folder / "Learning_exercise.ipynb").read_text())
    assert notebook["nbformat"] == 4
    todos = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        assert not cell["outputs"] and cell["execution_count"] is None, "Week 6 notebook has saved answers"
        source = "".join(cell["source"])
        ast.parse(source)
        if "# TO DO" in source:
            todos += 1
            assert not ast.parse(source).body, "Week 6 notebook TODO contains an answer"
    assert todos == 5, "Expected five clean notebook TODO cells"
    defined = functions(folder / "learning_by_hand.py")
    for name in ("squared_distance", "knn_predict", "accuracy", "holdout_split",
                 "perceptron_update", "train_perceptron", "k_fold_accuracy"):
        body = list(defined[name].body)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            body.pop(0)
        assert len(body) == 1 and isinstance(body[0], ast.Raise), f"Week 6 {name} must be a clean stub"
        exc = body[0].exc
        assert isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == "NotImplementedError", f"Week 6 {name} must remain unimplemented"
        assert len(exc.args) == 1 and isinstance(exc.args[0], ast.Constant) and isinstance(exc.args[0].value, str)
        assert not exc.keywords
    assert (folder / "week6_tuesday_code_card.pdf").read_bytes().startswith(b"%PDF-")


def main() -> None:
    files = public_files()
    check_paths(files)
    check_python_boundaries()
    check_mastermind_boundary()
    check_learning_boundary()
    print(f"Student release boundary verified across {len(files)} files.")


if __name__ == "__main__":
    main()
