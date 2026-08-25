# Degrees of Separation — student starter

Degrees models people as states and shared films as connections. Your task is
to implement a shortest-path search in `shortest_path()` inside `degrees.py`.

## Before the Tuesday studio

1. Watch the Search lecture and read the current Moodle preparation task.
2. Run the starter with the small dataset:

   ```bash
   cd Search
   python3 degrees.py small
   ```

3. Locate `shortest_path()` in `degrees.py` and the frontier classes in
   `util.py`.
4. Bring pseudocode explaining how you will:
   - add the initial node to the frontier;
   - distinguish frontier states from explored states;
   - reconstruct `(movie_id, person_id)` pairs using parent links; and
   - terminate when no connection exists.

You do not need a completed implementation before class. The protected core
uses `small/`; the much larger optional dataset is not included in this
release.

The project is adapted from Harvard's
[CS50 AI Degrees project](https://cs50.harvard.edu/ai/projects/0/degrees/).
Keep the supplied function signatures unchanged.
