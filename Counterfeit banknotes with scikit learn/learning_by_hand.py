#!/usr/bin/env python3
"""Learning by hand: nearest neighbours, the perceptron and honest testing.

Optional, ungraded consolidation; not a final-assignment prerequisite.
Choose steps to practise at your own pace.

Follow-up practice for Week 6 Tuesday (lecture "Learning - part1": k-nearest
neighbours, the perceptron, loss, overfitting, holdout and k-fold
cross-validation). Standard library only.

In class you classified new days by hand with 1-NN and 3-NN, traced the
perceptron learning rule row by row, and compared training accuracy with
holdout accuracy. In the lab, scikit-learn did the same things in one line
each. Here you write those lines yourself, so that nothing in
`model.fit(...)` and `model.predict(...)` stays a mystery. At the end your own
code runs on the real banknotes data.


The small example used in the docstrings
----------------------------------------
A gardener logs six days for a tomato plant. Two features per day:

    x1 = days since the plant was last watered
    x2 = hours of sunshine yesterday

and a label: 1 = "the plant needed water", 0 = "it was fine".

    features  label           x2
    (1, 1)    0  fine          4 |  .   .   .   1
    (2, 1)    0  fine          3 |  0   .   .   .   1
    (1, 3)    0  fine          2 |  .   .   .   1
    (4, 4)    1  water         1 |  0   0   .   .
    (5, 3)    1  water           +------------------ x1
    (4, 2)    1  water              1   2   3   4   5

These are PLANT below. Every worked example can be checked on paper.


How to work through this file
-----------------------------
There are seven small steps. Each step is one function marked TODO, and each
one matches something you did on the worksheet or the code card:

    Step 1  squared_distance    how far apart two examples are   (worksheet Task 3)
    Step 2  knn_predict         k-nearest-neighbour vote         (Task 3)
    Step 3  accuracy            fraction correct = 1 - 0-1 loss  (Task 9)
    Step 4  holdout_split       training set and test set        (Task 9, slide 88)
    Step 5  perceptron_update   one row of the perceptron trace  (Task 4)
    Step 6  train_perceptron    many rows: learn the weights     (Tasks 4-5)
    Step 7  k_fold_accuracy     k-fold cross-validation          (Task 11, slide 89)

Each step gives you
    * a plain description of what the function must do,
    * a worked example by hand, with numbers you can check on paper,
    * a code skeleton in comments. Delete the `raise NotImplementedError` line,
      uncomment the skeleton and fill in every ___ blank.

After every step, run

    python3 learning_by_hand.py

The file checks your steps in order, says which ones pass, and names the next
step. When all seven pass, it runs your code on banknotes.csv (it must be in
the same folder as this file) and prints a table of this shape (your numbers
are the ones that matter):

    holdout split: 824 training notes, 548 test notes
    model                    features   train acc   test acc
    1-NN                     all four   1.000       0.xxx
    ...

Finally, answer the three questions in the REFLECTION block at the bottom.

Do not change the constants or the functions marked GIVEN.
"""

import csv
import random
import sys
from pathlib import Path

# --- Data (do not change) ----------------------------------------------------
# (features, label): features = (days since watering, hours of sun yesterday)
PLANT = [
    ((1, 1), 0), ((2, 1), 0), ((1, 3), 0),
    ((4, 4), 1), ((5, 3), 1), ((4, 2), 1),
]

BANKNOTES = Path(__file__).resolve().parent / "banknotes.csv"
FEATURE_NAMES = ("variance", "skewness", "curtosis", "entropy")


# --- Given helpers -----------------------------------------------------------

def load_banknotes(path=BANKNOTES):
    """GIVEN. Read banknotes.csv into a list of (features, label).

    features is a tuple of four floats (variance, skewness, curtosis, entropy);
    label is 0 (authentic) or 1 (counterfeit).
    """
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)                      # skip the header row
        return [(tuple(float(cell) for cell in row[:4]), int(row[4])) for row in reader]


def keep_features(examples, columns):
    """GIVEN. Keep only some feature columns, e.g. columns=(0, 1) for variance and skewness."""
    return [(tuple(x[c] for c in columns), y) for x, y in examples]


def perceptron_predict(w, x):
    """GIVEN. The perceptron's hard threshold (lecture slide 39).

    w = (w0, w1, ..., wn) and x = (x1, ..., xn) WITHOUT the leading 1.
    h_w(x) = 1 if w0*1 + w1*x1 + ... + wn*xn >= 0, and 0 otherwise.

    Worked example: w = (-5, 1, 1), x = (4, 2): -5 + 4 + 2 = 1 >= 0  ->  1.
    """
    total = w[0] + sum(wi * xi for wi, xi in zip(w[1:], x))
    return 1 if total >= 0 else 0


# --- Step 1 ------------------------------------------------------------------

def squared_distance(a, b):
    """TODO 1. The squared (Euclidean) distance between two feature tuples.

    Subtract feature by feature, square each difference, and add the squares:
        (a1 - b1)**2 + (a2 - b2)**2 + ...
    It works for any number of features.

    Why squared? To find the NEAREST example we only compare distances, and
    squaring does not change which distance is smallest (worksheet Task 3), so
    we can skip the square root.

    Worked example by hand: a = (1, 2), b = (4, 6):
        (1 - 4)**2 + (2 - 6)**2 = 9 + 16 = 25      (the distance itself is 5)
    """
    # total = 0
    # for ai, bi in zip(a, b):          # one pair of features at a time
    #     total += ___
    # return total
    raise NotImplementedError("TODO 1: squared distance between two examples")


# --- Step 2 ------------------------------------------------------------------

def knn_predict(train, x, k):
    """TODO 2. Predict the label of x by a vote of its k nearest neighbours.

    train is a list of (features, label). Sort the training examples by their
    squared distance to x, take the first k, and return the most common label
    among them (lecture slides 27 and 34).

    Two rules for ties, so everybody gets the same answer:
      * Equal distances: keep the order of `train`. Python's sorted() is
        stable, so sorting by distance alone does exactly this.
      * Equal votes (possible when k is even): return the label of the nearest
        of the tied neighbours, i.e. the tied label that comes first in the
        sorted list.

    Worked example by hand, PLANT, new day x = (2, 4):
        squared distances: (1,3) -> 2 [label 0], (4,4) -> 4 [1], (4,2) -> 8 [1],
                           (2,1) -> 9 [0], (1,1) -> 10 [0], (5,3) -> 10 [1]
        k = 1: nearest label 0                  -> predict 0 (fine)
        k = 3: labels 0, 1, 1; label 1 wins 2-1 -> predict 1 (needs water)
    Like day B on the worksheet: k = 1 and k = 3 disagree.
    """
    # ranked = sorted(train, key=lambda example: squared_distance(example[0], ___))
    # labels = [label for _, label in ranked[:___]]        # labels of the k nearest
    # counts = {}
    # for label in labels:
    #     counts[label] = counts.get(label, 0) + 1
    # top = max(counts.values())
    # for label in labels:                                 # nearest first
    #     if counts[label] == ___:
    #         return label
    raise NotImplementedError("TODO 2: k-nearest-neighbour vote")


# --- Step 3 ------------------------------------------------------------------

def accuracy(model_predict, examples):
    """TODO 3. The fraction of examples a model labels correctly.

    model_predict is a function: give it the features, it returns a label.
    For each (features, label) in examples, compare model_predict(features)
    with the true label. Return (number correct) / (number of examples).

    This is 1 minus the average 0-1 loss (lecture slide 66): each example costs
    0 if the prediction is right and 1 if it is wrong.

    Worked example by hand, PLANT, with the rule "needs water if x2 >= 3":
        (1,1) 0 -> 0 right   (2,1) 0 -> 0 right   (1,3) 0 -> 1 WRONG
        (4,4) 1 -> 1 right   (5,3) 1 -> 1 right   (4,2) 1 -> 0 WRONG
    4 right out of 6: accuracy 4/6 = 0.667 (and average 0-1 loss 2/6).
    """
    # correct = 0
    # for features, label in examples:
    #     if ___ == label:
    #         correct += 1
    # return ___ / ___
    raise NotImplementedError("TODO 3: accuracy = fraction of correct predictions")


# --- Step 4 ------------------------------------------------------------------

def holdout_split(examples, test_fraction, rng):
    """TODO 4. Split the data into a training set and a test set (holdout).

    Learning happens on the training set; the test set is kept aside and used
    only to measure (lecture slide 88).

      1. Make a COPY of examples (do not reorder the caller's list).
      2. Shuffle the copy once with rng.shuffle(copy), so the test set is not
         just "the last rows of the file".
      3. n_test = int(len(examples) * test_fraction)
      4. The first n_test examples of the shuffled copy are the test set; the
         rest is the training set.
    Return (train, test).

    Worked example by hand: 10 examples, test_fraction = 0.4:
        n_test = int(10 * 0.4) = 4  ->  4 test examples, 6 training examples,
        and every example is in exactly one of the two sets.
    """
    # shuffled = list(___)                  # a copy
    # rng.shuffle(shuffled)
    # n_test = int(len(examples) * ___)
    # test = shuffled[:n_test]
    # train = shuffled[___:]
    # return train, test
    raise NotImplementedError("TODO 4: holdout split into training and test sets")


# --- Step 5 ------------------------------------------------------------------

def perceptron_update(w, x, y, alpha):
    """TODO 5. One row of the perceptron trace: return the NEW weights.

    w = [w0, w1, ..., wn] and x = (x1, ..., xn) WITHOUT the leading 1.
    Put the 1 in front yourself: the input vector is (1, x1, ..., xn), so that
    w0 is multiplied by 1 (lecture slide 38).

    Perceptron learning rule (slide 40), for every i including i = 0:
        wi  <-  wi + alpha * (y - h_w(x)) * xi
    where h_w(x) = 1 if w . x >= 0, else 0 (use perceptron_predict).
    If the prediction is right, y - h is 0 and nothing changes.
    Return a new list; do not change w itself.

    Worked example by hand, alpha = 1 (the first rows of PLANT):
        w = [0, 0, 0],    x = (1, 1), y = 0:
            w . (1, 1, 1) = 0 >= 0, so h = 1;  y - h = -1
            new w = [0 - 1, 0 - 1, 0 - 1] = [-1, -1, -1]
        w = [-1, -1, -1], x = (4, 4), y = 1:
            -1 - 4 - 4 = -9 < 0, so h = 0;     y - h = +1
            new w = [-1 + 1, -1 + 4, -1 + 4] = [0, 3, 3]
    """
    # inputs = (1,) + tuple(x)                   # the leading 1 for w0
    # error = y - perceptron_predict(w, x)       # +1, 0 or -1
    # return [wi + ___ * error * xi for wi, xi in zip(w, ___)]
    raise NotImplementedError("TODO 5: one perceptron update")


# --- Step 6 ------------------------------------------------------------------

def train_perceptron(examples, alpha, epochs):
    """TODO 6. Learn perceptron weights from examples.

    Start from all-zero weights: one weight per feature plus w0, so
    len(features) + 1 zeros. Then make `epochs` passes through the examples, in
    the order given, applying perceptron_update to each example. Return the
    final weights.

    Worked example by hand, PLANT, alpha = 1, one pass (epochs = 1):
        start          [0, 0, 0]
        (1,1) 0: sum 0,   h 1, wrong -> [-1, -1, -1]
        (2,1) 0: sum -4,  h 0, right -> unchanged
        (1,3) 0: sum -5,  h 0, right -> unchanged
        (4,4) 1: sum -9,  h 0, wrong -> [0, 3, 3]
        (5,3) 1: sum 24,  h 1, right -> unchanged
        (4,2) 1: sum 18,  h 1, right -> unchanged
    After one pass: [0, 3, 3]. That line still calls (1,1) "needs water"
    (0 + 3 + 3 >= 0), so more passes are needed. PLANT is linearly separable
    (slide 52), so the perceptron eventually stops making mistakes.
    """
    # n_features = len(examples[0][0])
    # w = [0] * (___ + 1)
    # for _ in range(epochs):
    #     for x, y in examples:
    #         w = perceptron_update(w, x, y, ___)
    # return w
    raise NotImplementedError("TODO 6: train the perceptron for several passes")


# --- Step 7 ------------------------------------------------------------------

def k_fold_accuracy(examples, k_neighbours, folds):
    """TODO 7. k-fold cross-validation of k-NN (lecture slide 89).

    Cut the examples, in their given order, into `folds` contiguous blocks of
    size = len(examples) // folds; the LAST block also takes any leftover
    examples. For each block in turn:
        test  = that block,
        train = all other examples,
        score = accuracy of k-NN (with k_neighbours) trained on train, on test.
    Return the average of the `folds` scores. Every example is tested exactly
    once, and never by a model that saw it during training.

    Worked example by hand, PLANT, 3 folds of 2, k_neighbours = 1:
        fold 1: test (1,1),(2,1)  train the other four
                (1,1): nearest (1,3) [d 4] -> 0 right
                (2,1): (1,3) and (4,2) both at d 5; (1,3) comes first -> 0 right
                score 2/2
        fold 2: test (1,3),(4,4)  train (1,1),(2,1),(5,3),(4,2)
                (1,3): nearest (1,1) [d 4] -> 0 right
                (4,4): nearest (5,3) [d 2] -> 1 right          score 2/2
        fold 3: test (5,3),(4,2)  train (1,1),(2,1),(1,3),(4,4)
                (5,3): nearest (4,4) [d 2] -> 1 right
                (4,2): nearest (4,4) [d 4] -> 1 right          score 2/2
        average (1 + 1 + 1) / 3 = 1.0

    Now try 2 folds of 3: the first block is (1,1),(2,1),(1,3), all "fine", so
    its training set holds only "needs water" days and every prediction is
    wrong. The same happens to the second block: the average is 0.0. Contiguous
    blocks of sorted data are a trap, which is why real data is shuffled first
    (Step 4).
    """
    # size = len(examples) // folds
    # scores = []
    # for i in range(folds):
    #     start = i * size
    #     end = len(examples) if i == folds - 1 else ___      # the last block takes the rest
    #     test = examples[start:end]
    #     train = examples[:start] + examples[___:]
    #     predict = lambda x: knn_predict(train, x, k_neighbours)
    #     scores.append(accuracy(predict, ___))
    # return sum(scores) / len(scores)
    raise NotImplementedError("TODO 7: k-fold cross-validation")


# --- Checks (GIVEN) ----------------------------------------------------------

class ScriptedRandom:
    """GIVEN. A stand-in for random.Random whose shuffle() reverses the list, so a
    check can see exactly which list was shuffled and how often."""

    def __init__(self):
        self.calls = 0

    def shuffle(self, values):
        self.calls += 1
        values.reverse()


def check_step1():
    """GIVEN."""
    d = squared_distance((1, 2), (4, 6))
    assert d != 5, "you returned the distance 5; return the SQUARED distance 25 (no square root)"
    assert d != 7, "7 is |1-4| + |2-6|, the sum of absolute differences; square each difference instead"
    assert d == 25, f"(1-4)**2 + (2-6)**2 = 25; you got {d}"
    assert squared_distance((4, 6), (1, 2)) == 25, "the order of a and b must not matter"
    assert squared_distance((0, 0, 0, 0), (1, 2, 2, 0)) == 9, "use every feature: 4 features here, 1+4+4+0 = 9"
    assert squared_distance((2, 1), (2, 1)) == 0, "an example is at distance 0 from itself"
    return "squared_distance((1, 2), (4, 6)) = 25"


def check_step2():
    """GIVEN."""
    before = list(PLANT)
    k1 = knn_predict(PLANT, (2, 4), 1)
    assert PLANT == before, "do not reorder or change the training list; sorted() makes a new list"
    assert k1 == 0, f"k = 1 at (2, 4): the nearest day is (1, 3), label 0; you got {k1}"
    k3 = knn_predict(PLANT, (2, 4), 3)
    assert k3 == 1, (f"k = 3 at (2, 4): the three nearest labels are 0, 1, 1, so 1 wins; you got {k3}. "
                     "Do you take exactly the k nearest?")
    assert knn_predict(PLANT, (2, 4), 6) == 0, "k = 6 uses all six days: three 0s and three 1s tie, and the nearest (label 0) decides"
    tied = [((0, 1), 1), ((1, 0), 0), ((0, -1), 0)]
    assert knn_predict(tied, (0, 0), 1) == 1, ("three examples at the same distance: keep the order of train, "
                                               "so the first one, label 1, is the nearest")
    assert knn_predict(PLANT, (3, 1), 2) == 0, ("k = 2 at (3, 1): labels 0 (d 1) and 1 (d 2) tie 1-1; "
                                                "return the label of the nearer one, 0")
    return "k = 1 says fine, k = 3 says needs water at (2, 4)"


def check_step3():
    """GIVEN."""
    rule = lambda x: 1 if x[1] >= 3 else 0
    a = accuracy(rule, PLANT)
    assert a != 4, "return a fraction of the examples (4/6), not the count 4"
    assert abs(a - 2 / 6) > 1e-9, "2/6 is the error rate (the average 0-1 loss); accuracy is the fraction CORRECT"
    assert abs(a - 4 / 6) < 1e-9, f"the rule x2 >= 3 is right on 4 of the 6 PLANT days; you got {a}"
    assert accuracy(lambda x: 0, PLANT[:3]) == 1, "a model that is right on every example has accuracy 1"
    return "accuracy of the rule 'x2 >= 3' on PLANT is 4/6"


def check_step4():
    """GIVEN."""
    examples = [((i, i), i % 2) for i in range(10)]
    before = list(examples)
    rng = ScriptedRandom()
    result = holdout_split(examples, 0.4, rng)
    assert examples == before, "you shuffled the caller's list; shuffle a COPY (list(examples)) instead"
    assert isinstance(result, tuple) and len(result) == 2, "return (train, test)"
    train, test = result
    assert rng.calls == 1, f"call rng.shuffle exactly once; you called it {rng.calls} times"
    assert len(test) == 4 and len(train) == 6, (f"10 examples with test_fraction 0.4 give 4 test and 6 training "
                                                f"examples; you got {len(test)} test and {len(train)} training")
    assert sorted(train + test) == sorted(examples), "every example must be in exactly one of the two sets"
    shuffled = examples[::-1]                 # what ScriptedRandom.shuffle does to the copy
    assert test == shuffled[:4], "the test set is the FIRST n_test examples of the shuffled copy"
    assert train == shuffled[4:], "the training set is everything after the first n_test examples"
    train, test = holdout_split(examples, 0.25, random.Random(1))
    assert len(test) == 2, "n_test = int(len(examples) * test_fraction): int(10 * 0.25) = 2"
    return "4 test and 6 training examples, from a shuffled copy"


def check_step5():
    """GIVEN."""
    w = [0, 0, 0]
    new = perceptron_update(w, (1, 1), 0, 1)
    assert w == [0, 0, 0], "do not change w in place; build and return a new list"
    assert new is not None and len(new) == 3, ("return one weight per input PLUS w0: three weights for two features. "
                                               "Did you prepend the 1 to x?")
    assert list(new) != [0, 0, 0], ("w . x = 0 here, and 0 >= 0 means h = 1 (slide 39), so this prediction is wrong "
                                    "and the weights must change. Do you use perceptron_predict (>= 0)?")
    assert list(new) != [1, 1, 1], "wrong direction: y - h = 0 - 1 = -1, so every weight goes DOWN by x_i"
    assert list(new) != [0, -1, -1], "w0 did not change: the input vector is (1, x1, x2), so w0 moves by alpha*(y-h)*1"
    assert list(new) == [-1, -1, -1], f"the worked example gives [-1, -1, -1]; you got {new}"
    assert list(perceptron_update([-1, -1, -1], (4, 4), 1, 1)) == [0, 3, 3], \
        "the second worked row: sum -9, h = 0, y - h = +1, so add x: [0, 3, 3]"
    half = list(perceptron_update([-1, -1, -1], (4, 4), 1, 0.5))
    assert half == [-0.5, 1, 1], f"with alpha = 0.5 the step is half as big: [-0.5, 1, 1]; you got {half}. Use alpha."
    assert list(perceptron_update([0, 3, 3], (5, 3), 1, 1)) == [0, 3, 3], "a correct prediction (y - h = 0) changes nothing"
    return "both worked rows reproduced: [-1, -1, -1], then [0, 3, 3]"


def check_step6():
    """GIVEN."""
    one = train_perceptron(PLANT, 1, 1)
    assert one is not None and len(one) == 3, "start from len(features) + 1 zeros: three weights for two features"
    assert list(one) != [0, 0, 0], "no update happened: did you call perceptron_update for every example?"
    assert list(one) == [0, 3, 3], (f"one pass over PLANT in the given order gives [0, 3, 3] (the worked table); "
                                    f"you got {one}. Do you start from zeros and keep the order of the examples?")
    two = train_perceptron(PLANT, 1, 2)
    assert list(two) == [-2, 3, 2], (f"two passes give [-2, 3, 2]; you got {two}. Does each pass start from the weights "
                                     "the previous pass ended with (not from zeros)?")
    w = train_perceptron(PLANT, 1, 20)
    right = sum(perceptron_predict(w, x) == y for x, y in PLANT)
    assert right == 6, f"after 20 passes the line should separate all six PLANT days; it gets {right} right"
    return f"after 20 passes w = {list(w)} separates all six PLANT days"


def check_step7():
    """GIVEN."""
    score = k_fold_accuracy(PLANT, 1, 3)
    assert score is not None, "return the average score"
    assert abs(score - 1) < 1e-9, (f"the worked example (3 folds of 2, k = 1) gives (1 + 1 + 1) / 3 = 1.0; you got "
                                   f"{score:.3f}. Check the block boundaries: fold i tests examples[i*size:(i+1)*size]")
    two = k_fold_accuracy(PLANT, 1, 2)
    assert abs(two) < 1e-9, (f"2 folds of 3 must give 0.0 (see the docstring); you got {two:.3f}. Is the test block "
                             "left out of the training set, and do you keep the examples in their given order?")
    seven = PLANT + [((3, 2), 1)]
    score = k_fold_accuracy(seven, 1, 3)
    assert abs(score - 13 / 18) < 1e-9, (
        f"7 examples in 3 folds: blocks of 2, 2 and 3 (the last block takes the leftover); expected 0.722, "
        f"got {score:.3f}. Is the leftover example tested, and never also in the training set?")
    return "3 folds give 1.0 and 2 folds give 0.0 on PLANT: fold boundaries matter"


CHECKS = (check_step1, check_step2, check_step3, check_step4, check_step5, check_step6, check_step7)


def run_checks():
    """GIVEN. Check the steps in order; stop at the first one that is not done."""
    for number, check in enumerate(CHECKS, start=1):
        try:
            message = check()
        except NotImplementedError as todo:
            print(f"\nStep {number} is next: {todo}")
            print("Read its docstring, delete the raise line, and fill in the skeleton.")
            return False
        except AssertionError as problem:
            print(f"Step {number}  NOT YET: {problem}")
            return False
        print(f"Step {number}  PASS  {message}")
    print()
    return True


def main():
    """GIVEN. Check every step, then run your code on the banknotes data."""
    if not run_checks():
        sys.exit(1)
    if not BANKNOTES.exists():
        print(f"All steps pass. Put banknotes.csv next to this file to run on real data ({BANKNOTES}).")
        sys.exit(1)
    notes = load_banknotes()
    train, test = holdout_split(notes, 0.4, random.Random(0))
    print(f"holdout split: {len(train)} training notes, {len(test)} test notes")
    print(f"{'model':<24} {'features':<10} {'train acc':<11} test acc")
    for columns, label in (((0, 1, 2, 3), "all four"), ((0, 1), "two")):
        tr, te = keep_features(train, columns), keep_features(test, columns)
        for k in (1, 3):
            predict = lambda x, tr=tr, k=k: knn_predict(tr, x, k)
            print(f"{f'{k}-NN':<24} {label:<10} {accuracy(predict, tr):<11.3f} {accuracy(predict, te):.3f}")
    w = train_perceptron(train, 0.01, 10)
    predict = lambda x: perceptron_predict(w, x)
    print(f"{'perceptron (10 passes)':<24} {'all four':<10} {accuracy(predict, train):<11.3f} {accuracy(predict, test):.3f}")
    print()
    subset = keep_features(notes[:600], (0, 1))
    print("5-fold cross-validation, two features, first 600 notes (to keep it fast):")
    for k in (1, 3, 15):
        print(f"  k = {k:<3} mean accuracy {k_fold_accuracy(subset, k, 5):.3f}")


if __name__ == "__main__":
    main()


# --- REFLECTION --------------------------------------------------------------
# Answer in two or three sentences each, using numbers from your table.
#
# 1. With only two features, compare 1-NN's training accuracy with its test
#    accuracy. Why is 1-NN's training accuracy always 1.000 (worksheet Task 9),
#    and what does the gap tell you?
#
#
# 2. Which k would you choose for the two-feature data, and why must that
#    choice come from the cross-validation numbers and not from training
#    accuracy?
#
#
# 3. The perceptron draws one straight line (slide 52). Look at its test
#    accuracy next to k-NN's. What can k-NN do that a single line cannot, and
#    what does a line give you that k-NN does not?
#
