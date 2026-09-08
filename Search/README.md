# Degrees of Separation

Degrees models people as states and shared films as connections. The task was
to implement a shortest-path search in `shortest_path()` inside `degrees.py`.

The deadline has passed, so `degrees.py` now contains a worked breadth-first
solution. Compare it with your own attempt: check where you tested for the
goal, how you kept frontier states apart from explored ones, and how the
`(movie_id, person_id)` path was reconstructed.

## How the task was set up

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

The released solution uses `small/`; the much larger optional dataset is not
included in this release.

The project is adapted from Harvard's
[CS50 AI Degrees project](https://cs50.harvard.edu/ai/projects/0/degrees/).
Keep the supplied function signatures unchanged.
