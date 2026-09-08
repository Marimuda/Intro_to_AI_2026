# Tic-Tac-Toe

This project represents Tic-Tac-Toe as a deterministic, adversarial search
problem, built from seven functions in `tictactoe.py`:

- `player`
- `actions`
- `result`
- `winner`
- `terminal`
- `utility`
- `minimax`

The deadline has passed, so a worked implementation is now released, with
`max_value` and `min_value` as the two halves of the Minimax recursion. Read
the first six functions as states, actions, terminal tests, and utility before
reading `minimax` itself.

## Setup

From this directory, create an isolated environment and install Pygame:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m py_compile tictactoe.py runner.py
```

Then launch the interface with:

```bash
python runner.py
```

The project is adapted from Harvard's
[CS50 AI Tic-Tac-Toe project](https://cs50.harvard.edu/ai/projects/0/tictactoe/).
Keep the constants and public function signatures unchanged. You will still be
asked to explain and vary the algorithm, so work through it rather than around
it.
