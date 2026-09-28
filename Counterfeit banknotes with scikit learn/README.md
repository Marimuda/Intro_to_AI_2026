# Week 6 — Learning from examples

Tuesday's banknotes lab uses four measured features and the supplied label:
0 = authentic, 1 = counterfeit. The CSV has 1372 rows plus a header.

## Tuesday lab

1. Keep `banknotes.csv` beside your program or notebook.
2. Use Python 3.10 or newer with scikit-learn. Check the same environment you
   will use in class: `python3 -c "import sklearn; print(sklearn.__version__)"`.
   If needed, install there with `python3 -m pip install scikit-learn`.
   In Jupyter, check the notebook kernel rather than assuming it matches a terminal.
3. Open `week6_tuesday_code_card.pdf`. Task 12 is the core tournament;
   Task 13 and the cross-validation sweep are extensions if time.
   Start `tournament.py` from the code card, or use a notebook cell.
4. Alternatively, `Learning_exercise.ipynb` provides the original guided
   single-model scaffold. Use one route; completing both is not required.
5. Compare training and holdout scores. If those scores choose a model,
   treat them as validation evidence; a final performance claim needs an
   untouched test. This lab is an exploratory teaching comparison.

If local setup fails, upload the notebook and CSV to Colab's Files panel.
Keep the CSV in the notebook's working directory. In class you can also work
with a partner as the auditor while they run the code.

## Optional consolidation

`learning_by_hand.py` has seven small TODO steps and checks them in order.
Choose steps you want to practise after class and run
`python3 learning_by_hand.py` after each change. An untouched file stops at
TODO 1 with a message naming the next step; that is expected.

This follow-up is **optional and ungraded**. It is not another hand-in or a
prerequisite for the final assignment, which supplies its own predictors.
Moodle gives the course's required work, dates and permitted-tool rules.

## Data and attribution

The notebook and CSV are adapted from Harvard's CS50 Introduction to
Artificial Intelligence with Python: <https://cs50.harvard.edu/ai/>.
The CSV was recovered from the 2020 course source bundle
(`src4/banknotes/banknotes.csv`) without changing the data.
CS50 materials use CC BY-NC-SA 4.0; see the repository's licence and
third-party notices. The local code card and optional practice scaffold
support the Week 6 lesson.
