# Day 1: Setup & Introduction

Welcome to Capitalism simulator!! Today we learn Python fundamentals - variables, comments,
printing, errors, arithmetic, and data types - by exploring and editing our game. Work
through the steps **in order**; each one builds on the last.

> **How to find each spot:** open the file named in the step and use your editor's
> Find (Ctrl+F / Cmd+F) to search for the `@STUDENT-EDIT-...` marker.

## Step 1: Examine Variables and Datatypes
Open `settings.py` and find `@STUDENT-EDIT-Day1-1`.
A **variable** is a name for a value. Identify the datatypes being used: `SCREEN_WIDTH` is an **integer** (a whole number), while `TITLE` is a **string** (text in quotes).

## Step 2: Add a Comment
Still at `@STUDENT-EDIT-Day1-1` in `settings.py`.
A **comment** starts with `#` - Python **ignores everything after the `#`**, so comments are notes for humans, not instructions for the computer. Write one above a variable to describe what it does:
```python
# The width of the screen is 1280 pixels
SCREEN_WIDTH = 1280
```
Good comments explain *why* something is done. You'll use them all week.

## Step 3: Customize the Game Window Title
Open `settings.py` and find `@STUDENT-EDIT-Day1-2`.
Change the `TITLE` variable to a **string** of your choice (text in quotes). Make it your own game!
```python
TITLE = "My Awesome Farm Game"
```

## Step 4: Change the Window Size
Open `settings.py` and find `@STUDENT-EDIT-Day1-3`.
`SCREEN_WIDTH` and `SCREEN_HEIGHT` are **integers** (whole numbers). Change them and notice how the window changes when you run the game.

## Step 5: Experiment with Background Colors
Open `settings.py` and find `@STUDENT-EDIT-Day1-4`.
Change `WATER_COLOR` to a different hex code like `"#FF0000"` for red or `"#00FF00"` for green.

## Step 6: Print to the Console
Open `main.py` and find `@STUDENT-EDIT-Day1-5` inside the `__init__` method.
`print()` is a built-in **function** that displays text. Add:
```python
print("Game starting!")
```
Run the game (`python main.py`) and check your console output!

## Step 7: Combine Text and Variables with f-strings
Open `main.py` and find `@STUDENT-EDIT-Day1-6` (right below the last step).
Often you want to print text **and** a variable together. Use an **f-string** (note the `f` before the quotes, and the `{ }` around the variable):
```python
print(f"Welcome to {TITLE}!")
```
Run the game - the `{TITLE}` gets replaced with your game's title.

## Step 8: Read Your First Error Message
Errors are normal - everyone gets them! In `main.py`, temporarily add a line that uses a variable that doesn't exist:
```python
print(favorite_game)
```
Run the game. You'll see a `NameError`. **Read the LAST line of the error message** - it tells you the type of error and what went wrong (`name 'favorite_game' is not defined`). Now delete that line to fix it. Learning to read errors is a core skill!

> **Order matters:** Python runs your file top to bottom, so a variable must be **created before it is used**. That's exactly why `print(favorite_game)` failed - nothing had defined `favorite_game` yet.

## Step 8a: Fixing Your First Error
Let's do a quick exercise to fix the error and synthesize what you've learned.
- In `main.py`, create the variable `favorite_game` and assign it a *string*.
- Create a print statement that displays the value of `favorite_game`.

## Step 9: Use Variables in Calculations
Open `settings.py` and find `@STUDENT-EDIT-Day1-8`.
Variables can be used in **math**. `SCREEN_CENTER_X` and `SCREEN_CENTER_Y` are calculated from the screen size using `/` (division). Try adding a line to print one of them, then change the screen size and see the center change too.

## Step 10: Order of Operations (Playground)
Open `scratch.py` and find `@STUDENT-EDIT-Day1-9`. Run it with `python scratch.py`.
Python follows **PEMDAS** (Parentheses, Exponents, Multiply/Divide, Add/Subtract). Use `**` for powers - `^` does something totally different! Confirm the two exercises give `-5.0` and `9.75`, then try your own math.

## Step 11: Data Types and Type Casting
Open `scratch.py` and find `@STUDENT-EDIT-Day1-10` (and the matching note in `settings.py`).
Every value has a **type** (`int`, `float`, `str`, ...). Use `type()` to check it, and `int()` / `float()` to **convert** ("cast") between types. Notice that `int(3.99)` gives `3` - it *truncates*, it does **not** round!
