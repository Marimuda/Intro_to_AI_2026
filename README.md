# Intro to Artificial Intelligence 2026

This is the official student code repository for **5700.26 — Innleiðing í
tilgjørdum viti (Introduction to Artificial Intelligence)** at the University
of the Faroe Islands.

Moodle is the authoritative source for dates, preparation tasks, submissions,
and announcements. This repository is the code channel: new student material
will be added here as the course progresses.

## Current release

The repository currently contains the student starters for **Week 2 — Search
and Games**:

- `Search/` — Degrees of Separation, the core Tuesday studio task;
- `tic-tac-toe/` — the seven-function Minimax starter used for Thursday's
  representation work and optional extension.

Only the small Degrees dataset is included. It is sufficient for the required
lab and avoids a large download. Worked solutions appear here only after the
deadline for that task has passed; answer keys, instructor checks, future
assignments, and unreleased weeks are deliberately not part of this
repository.

## Get started

You need Git and Python 3. From a terminal:

```bash
git clone https://github.com/Marimuda/Intro_to_AI_2026.git
cd Intro_to_AI_2026
python3 --version
```

Check the starter without changing it:

```bash
cd Search
python3 degrees.py small
```

The program should load the data and ask for two names, then print the
connection between them. The Week 2 worked solutions for Degrees and
Tic-Tac-Toe are now released; read them against your own attempt rather than
in place of it.

See the README inside each exercise directory for its task and setup.

## Getting later releases

Moodle will say when a new folder is ready. If your checkout has no conflicting
local changes, update it with:

```bash
git pull
```

Keep your own work locally or in a **private** repository. Do not publish
completed coursework or make a public fork containing your answers.

## Course-work boundary

Your submitted work must be your own. You may discuss ideas and debugging, but
do not obtain, publish, or share completed implementations of tasks whose
deadline has not passed.
You should be able to explain, test, and vary your own code in class and in the
oral assessment. Follow the current Moodle policy for permitted tool and AI
use.

## Attribution and licence

Some starter material is adapted from Harvard's
[CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/),
which is licensed under CC BY-NC-SA 4.0. See [LICENSE](LICENSE) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for details.
