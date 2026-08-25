# Tic-Tac-Toe — student starter

This starter represents Tic-Tac-Toe as a deterministic, adversarial search
problem. Seven functions in `tictactoe.py` are intentionally unfinished:

- `player`
- `actions`
- `result`
- `winner`
- `terminal`
- `utility`
- `minimax`

For the required Thursday preparation, inspect what the first six function
contracts mean and connect them to states, actions, terminal tests, and utility.
A complete Minimax implementation is an extension rather than part of the
protected Week 2 core.

## Setup

From this directory, create an isolated environment and install Pygame:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m py_compile tictactoe.py runner.py
```

After implementing the required functions, launch the interface with:

```bash
python runner.py
```

The project is adapted from Harvard's
[CS50 AI Tic-Tac-Toe project](https://cs50.harvard.edu/ai/projects/0/tictactoe/).
Keep the constants and public function signatures unchanged. Do not use or
share a completed implementation; you will be asked to explain and vary your
algorithm.
