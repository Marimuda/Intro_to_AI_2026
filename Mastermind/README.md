# Mastermind — student exercise

Use propositional logic and model checking to infer the four-colour arrangement
from two clue rounds.

Student files:

- `mastermind_exercise.py` — six bounded TODO blocks;
- `logic.py` — supplied propositional-logic and model-checking library;
- `Mastermind.pdf` — inherited reference description; the A4 Week 3 workbook is
  the core classroom handout;
- `Logic_example.ipynb` — optional syntax examples.

Run from this directory with:

```bash
python3 mastermind_exercise.py
```

Record a prediction before each query run. A printed arrangement is not enough:
you must be able to identify which structural or clue constraint rules out an
alternative world.

The completed implementation is not distributed. Keep your own solution local
or in a private repository.

`logic.py` is the propositional-logic library from Harvard's
[CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/),
licensed under CC BY-NC-SA 4.0. Keep its class names and `model_check`
signature unchanged.
