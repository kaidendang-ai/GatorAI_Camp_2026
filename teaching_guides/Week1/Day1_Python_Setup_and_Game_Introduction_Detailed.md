# Day 1: Python Setup and Game Introduction

## Objective
Set up programming environment and begin coding fundamentals.

## Setup Tasks
1. **Install & Run IDE**: Explain what IDEs are and set up development environment. If everything went according to plan, this will already be done!
2. **Install Python**: Walk through Python installation. **Use Python 3.11 or 3.12** — the
   game's libraries (pygame-ce, torch, opencv) have prebuilt wheels for those versions.
   Very new versions (3.14) may not, and will try to compile from source and fail. Similar to Step 1, hopefully this is already done!
3. **GitHub Setup**: Sign-in or sign-up for GitHub account
4. **Download Project**: Fork from [The GitHub Repository](https://github.com/PracticumAI/GatorAI_Camp_2026)

## Core Concepts

### Basic Python Syntax
- Simple print statements and `#` comments
- Indentation rules in Python

### Variables & Data Types
- Integers, floats, strings, dictionaries
- The `type()` function and type casting (`int()`, `float()`)
- Assign simple values (character names, positions, etc.)

### Printing and f-strings
- `print()` to display text and variables; f-strings to combine them (`f"...{var}..."`)

### Reading Error Messages
- `NameError`, and reading the **last line** of a traceback

### Arithmetic
- Using variables in calculations; PEMDAS and `**` (with the `^`-is-XOR gotcha)

### Game Environment Overview
- Introduce existing game framework
- Show game file locations and how to run the game (`python main.py`)

### A First Look at Classes
- The `Game` class as a "blueprint"; `def __init__(self)` and `self`

## Exercise: Customize the Game
The student-facing steps for today live in
[student_tutorials/Day1_Basics.md](../../student_tutorials/Day1_Basics.md). Students
look for the `@STUDENT-EDIT-Day1-*` markers in the code and edit around them.
- **Deliverable**: Push project to personal GitHub repository

## Code References

> All snippets below are copied from the **actual** project files. Line numbers are
> approximate (the files change as students edit them) — search for the quoted code or
> the `@STUDENT-EDIT` marker rather than trusting an exact line.

### Main Entry Point and Dependency Installation
**File**: [main.py](../../main.py) (top of file)

The game starts in `main.py`. The very first thing it does is make sure the required
libraries are installed, using a small helper from `installer.py`:

```python
# Import required modules for our game
from installer import install

# Install required packages if they're not already installed
# (commented out by default - uncomment a line if the game reports a missing library)
# install("pygame-ce")  # Game development library (community fork, imports as "pygame")
# install("pytmx")  # Map loading library
# install("kagglehub")  # Dataset library
# install("requests")  # Library for web requests
# install("opencv-python")  # Computer vision library
# install("torchvision")
# install("pytorch_lightning")
# install("openai")  # AI API library for dialogue generation

import pygame  # Main game development library
import sys  # System operations
import os  # Operating system interface

# Import our custom game modules
from settings import *  # Game configuration settings
from main_menu import MainMenu  # Main menu system
import game_settings  # Audio and game settings
from collections import deque
```

**DETAILED WALKTHROUGH:**

1. **`from installer import install`** — imports a custom function from our own
   `installer.py` file. This is an example of *code reuse*: using code we wrote in
   another file.

2. **The `install(...)` calls (commented out by default)** — each one *would* check
   whether a library is present and install it if not. They ship commented out because
   the camp machines already have the core libraries; uncomment a line if the game
   reports that library missing. Note `install("pygame-ce")`: the community fork of
   pygame still imports as `import pygame` — a package's *install name* and its
   *import name* can differ.

3. **Standard library imports (`pygame`, `sys`, `os`)** — `pygame` is the game engine,
   `sys` is used for `sys.exit()`, and `os` is used to work with file paths.

4. **Custom module imports** — `from settings import *`, `from main_menu import MainMenu`,
   `import game_settings`, and `from collections import deque`. Today students just
   *notice* these lines exist; the three import **styles** (and `help`/`dir`/aliases) are
   the formal **Day 2** libraries lesson.

### The Settings File (Variables & Data Types)
**File**: [settings.py](../../settings.py)

This is the best file for today's "variables and data types" lesson. It is full of
clearly-typed values students can read and change:

```python
# @STUDENT-EDIT-Day1-3: Change the game window size
SCREEN_WIDTH = 1280   # integer
SCREEN_HEIGHT = 720   # integer
# @STUDENT-EDIT-Day1-2: Customize the game window title (TITLE)
TITLE = "Capitalism simulator!"   # string
# @STUDENT-EDIT-Day1-4: Experiment with different background colors
WATER_COLOR = "#71ddee"   # string holding a hex color code
TILE_SIZE = 64   # integer
```

**DETAILED WALKTHROUGH:**
- `SCREEN_WIDTH` / `SCREEN_HEIGHT` / `TILE_SIZE` are **integers**.
- `TITLE` and `WATER_COLOR` are **strings**.
- Later in the file, `SALE_PRICES` and `GROW_SPEED` are **dictionaries**, and
  `APPLE_POS` is a dictionary of **lists of tuples** — good examples to point at when
  introducing data structures.
- The `@STUDENT-EDIT-Day1-*` comments mark exactly where students should make their
  Day 1 edits (window title, window size, background color).

### Comments
**File**: [settings.py](../../settings.py) — marker `@STUDENT-EDIT-Day1-1`

At the same marker where students read the typed constants, they write their first
comment (Day 1 tutorial Step 2):

```python
# The width of the screen is 1280 pixels
SCREEN_WIDTH = 1280
```

**DETAILED WALKTHROUGH:**
- Anything after a `#` on a line is a **comment** — Python ignores it entirely. Comments
  are notes for humans (and your future self), not instructions for the computer.
- Teach the habit early: "comment the *why*, not the obvious." This is the concept's
  home; Day 2 only briefly revisits good commenting alongside the other style topics.

### Printing and f-strings
**File**: [main.py](../../main.py) — `Game.__init__`

Two adjacent markers introduce output. `@STUDENT-EDIT-Day1-5` adds a plain print;
`@STUDENT-EDIT-Day1-6` introduces the f-string:

```python
        # @STUDENT-EDIT-Day1-5: ... print("Game starting!")
        # @STUDENT-EDIT-Day1-6: ... print(f"Welcome to {TITLE}!")
```

**DETAILED WALKTHROUGH:**
- `print("Game starting!")` displays literal text — the first thing to add so students
  see the console react to their code.
- `print(f"Welcome to {TITLE}!")` is a **formatted string literal (f-string)**: the `f`
  before the quote lets you drop a variable inside `{ }`. `TITLE` comes from
  `settings.py`, so the printed line changes when they change the title. This is the
  cleanest way to combine text and variables and is used all over the codebase.

### Reading Error Messages (on purpose)
**File**: run from `main.py`

The notebook meets errors early, so Day 1 does too (the *deep* debugging day is Day 4).
Have students temporarily add a line that uses an undefined name (`@STUDENT-EDIT-Day1-7`
in the Day 1 tutorial is a do-then-undo step, not a permanent code marker):

```python
print(favorite_game)   # add this, run, read the error, then delete it
```

**DETAILED WALKTHROUGH:**
- The console shows `NameError: name 'favorite_game' is not defined`.
- Teach the habit: **read the last line first** — it names the error type and the
  problem. Reassure students that errors are normal and are the fastest way to learn.

### Variables in Calculations and PEMDAS
**Files**: [settings.py](../../settings.py) and [scratch.py](../../scratch.py)

`@STUDENT-EDIT-Day1-8` adds two computed constants — variables used in math:

```python
SCREEN_CENTER_X = SCREEN_WIDTH / 2   # float: horizontal middle of the screen
SCREEN_CENTER_Y = SCREEN_HEIGHT / 2  # float: vertical middle of the screen
```

**DETAILED WALKTHROUGH:**
- These show that variables can be **used in expressions**, and that division (`/`)
  always yields a `float`. The game centers UI with this same math, so it isn't busywork.
- For pure arithmetic practice (which has no game surface), `scratch.py`'s
  `@STUDENT-EDIT-Day1-9` holds two notebook exercises: `(100 - 5**3)/5 = -5.0` and
  `15/4 + 6 = 9.75`. **Key gotcha:** `**` is "to the power of"; `^` is *not* — it's a
  bitwise XOR. Python follows PEMDAS.

### Data Types and Type Casting
**Files**: [scratch.py](../../scratch.py) and [settings.py](../../settings.py)

`@STUDENT-EDIT-Day1-10` (a note in `settings.py`, with practice in `scratch.py`):

```python
print(type(SCREEN_WIDTH))     # <class 'int'>
print(type(SCREEN_CENTER_X))  # <class 'float'>  (division makes a float)
y = int(3.99)                 # 3  -> truncates toward zero, does NOT round!
z = float(3)                  # 3.0
```

**DETAILED WALKTHROUGH:**
- `type()` reveals a value's type; `int()`/`float()` **cast** between types.
- The most important insight (straight from the notebook): `int()` **truncates**, it
  does not round — `int(3.99)` is `3`. This surprises students and is worth demoing live.
- Tie-in: ML libraries are picky about types (e.g. models want floats/tensors), so
  casting is a constant chore in real AI work — previews Week 2.

### A First Look at Classes: the `Game` Class
**File**: [main.py](../../main.py) — `class Game`

A **class** is a *blueprint* that bundles data and behavior together; the entire game lives inside the
`Game` class. Students don't edit this today — they just meet the idea.

```python
class Game:
    """
    Main Game Class - The Heart of Our Game
    ======================================
    This class manages the entire game, including:
    - Starting up pygame and creating the game window
    - Managing the main menu and game screens
    - Running the main game loop
    - Handling user input and events
    """

    def __init__(self):
        # Initialize pygame - this must be done before using pygame features
        pygame.init()
        pygame.mixer.init()  # Initialize audio system for sound effects and music

        # Create the game window with specified dimensions
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)  # Set window title

        # Create a clock to control frame rate (how fast the game runs)
        self.clock = pygame.time.Clock()
```

**DETAILED WALKTHROUGH:**

1. **`class Game:`** — a class is a blueprint. Our `Game` class holds all the logic for
   starting and running the game.

2. **`def __init__(self):`** — the *constructor*, run automatically when we write
   `game = Game()` at the bottom of the file. `self` refers to the specific game object
   being built.

3. **`pygame.init()` and `pygame.mixer.init()`** — turn on the pygame engine and its
   audio system. These must happen before any other pygame call.

4. **`pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))`** — creates the window.
   `SCREEN_WIDTH` and `SCREEN_HEIGHT` are constants imported from `settings.py`
   (currently `1280` and `720`). The returned surface is stored in `self.screen` so we
   can draw on it later.

5. **`pygame.display.set_caption(TITLE)`** — sets the text in the window's title bar.
   `TITLE` is also from `settings.py`.

6. **`self.clock = pygame.time.Clock()`** — a clock used to cap the frame rate so the
   game runs at a steady speed on any computer.

### The Program Entry Point
**File**: [main.py](../../main.py) (bottom of file)

```python
if __name__ == "__main__":
    game = Game()  # Create a new Game instance
    game.run()     # Start the main game loop
```

**DETAILED WALKTHROUGH:**
- `if __name__ == "__main__":` is a standard Python idiom meaning "only run this when
  the file is executed directly (not imported)."
- `game = Game()` creates a Game object (which runs `__init__`).
- `game.run()` starts the main loop. Today, students just need to know this is where
  the game begins; `run()` is explored on later days.

## Key Learning Points
1. **How a Python program starts** — the `if __name__ == "__main__":` pattern and
   top-to-bottom execution (the notebook's "order of execution").
2. **Variables, comments, and data types** — reading/editing typed constants in
   `settings.py`; writing `#` comments; `type()` and casting, where `int()` truncates
   rather than rounds.
3. **Printing and f-strings** — `print()` and `f"...{var}..."` to combine text + values.
4. **Reading errors** — `NameError` and reading the last line of a traceback.
5. **Arithmetic** — variables in calculations, PEMDAS, and `**` vs the `^`-is-XOR gotcha.
6. **Imports are previewed, not taught yet** — students *notice* the `import` lines at
   the top of `main.py`; the formal libraries lesson is Day 2.
7. **A first look at classes (end of day)** — `class`, `def __init__(self)`, and `self`;
   the one bigger idea, introduced after the simpler fundamentals.
8. **Initializing pygame** — `pygame.init()`, `set_mode`, `set_caption`, the `Clock`
   (all inside the `Game` class's `__init__`).

## Extension Activities
1. **Add a comment** — write a `#` comment above a variable (`@STUDENT-EDIT-Day1-1`).
2. **Personalize the title** — change `TITLE` in [settings.py](../../settings.py)
   (`@STUDENT-EDIT-Day1-2`).
3. **Resize the window** — change `SCREEN_WIDTH` / `SCREEN_HEIGHT` (`@STUDENT-EDIT-Day1-3`).
4. **Change the water color** — try `WATER_COLOR = "#FF0000"` (`@STUDENT-EDIT-Day1-4`).
5. **Print when the game starts** — add `print("Game starting!")` at
   `@STUDENT-EDIT-Day1-5`.
6. **Print with an f-string** — add `print(f"Welcome to {TITLE}!")` at
   `@STUDENT-EDIT-Day1-6`.
7. **Trigger and read an error** — temporarily `print(favorite_game)`, read the
   `NameError`'s last line, then delete it.
8. **Fix the error** — create a `favorite_game` string variable and print its value.
9. **Compute a value** — inspect/print `SCREEN_CENTER_X`/`SCREEN_CENTER_Y`
   (`@STUDENT-EDIT-Day1-8`); resize the window and see them change.
10. **Run the playground** — `python scratch.py` and work the PEMDAS
    (`@STUDENT-EDIT-Day1-9`) and `type()`/casting (`@STUDENT-EDIT-Day1-10`) exercises.

## Troubleshooting Tips
- **pygame won't install / tries to "build a wheel":** you are probably on a too-new
  Python. Use Python 3.11 or 3.12. The project installs `pygame-ce`, which has wheels
  for those versions.
- **`ModuleNotFoundError`:** make sure you ran `python main.py` from inside the
  `GatorAI_Camp_2026` folder. If a library really is missing, uncomment its
  `install(...)` line at the top of `main.py` (they're commented out by default).
- **Window opens then closes instantly:** check the console for a Python error — a typo
  in `settings.py` (e.g. a missing quote) is the usual cause.
