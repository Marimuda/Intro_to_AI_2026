#!/usr/bin/env python3
"""Fail if the public checkout crosses the current student-solution boundary."""

from __future__ import annotations

import ast
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
TICTACTOE_STUBS = (
    "player",
    "actions",
    "result",
    "winner",
    "terminal",
    "utility",
    "minimax",
)


def public_files() -> list[Path]:
    """Return tracked files, or all candidate files before the first commit."""
    try:
        output = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        output = b""

    if output:
        return [ROOT / item.decode() for item in output.split(b"\0") if item]

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
    degrees = functions(ROOT / "Search" / "degrees.py")
    assert "shortest_path" in degrees, "Degrees shortest_path() is missing"
    assert is_clean_stub(degrees["shortest_path"]), (
        "Degrees shortest_path() must remain a clean starter stub"
    )

    tictactoe = functions(ROOT / "tic-tac-toe" / "tictactoe.py")
    assert set(TICTACTOE_STUBS) <= set(tictactoe), (
        "one or more required Tic-Tac-Toe functions are missing"
    )
    for name in TICTACTOE_STUBS:
        assert is_clean_stub(tictactoe[name]), (
            f"Tic-Tac-Toe {name}() must remain a clean starter stub"
        )


def main() -> None:
    files = public_files()
    check_paths(files)
    check_python_boundaries()
    print(f"Student release boundary verified across {len(files)} files.")


if __name__ == "__main__":
    main()
