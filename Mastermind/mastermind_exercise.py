from logic import *

# Define your symbols:
colors = ["red", "blue", "green", "yellow"]
symbols = []
for i in range(4):
    for color in colors:
        symbols.append(Symbol(f"{color}{i}"))

# Initialize your knowledge base:
knowledge = And()

# TODO 1: Encode that each color appears in at least one position.


# TODO 2: Encode that a color cannot occupy two different positions.


# TODO 3: Encode that one position cannot contain two different colors.


# TODO 4: Encode the first clue: exactly two of red0, blue1, green2,
# and yellow3 are true.


# TODO 5: Encode the second clue: none of blue0, red1, green2,
# and yellow3 is true.


# TODO 6: Query every symbol and print only those entailed by the knowledge base.


# Keep this check. It only fires while the knowledge base is still empty.
if not knowledge.conjuncts:
    print("The knowledge base is empty. Complete the six numbered tasks above, then run again.")
