# Day 1: Splash Screen Customization

Welcome to Day 1! Today we'll customize the PyDew Valley splash screen.

## Step 1: Change the Game Title
**File to edit:** `settings.py`
**Search for:** `@STUDENT-EDIT-Day1-1`

The game currently has a default title. Let's make it your own!
**Hint:** Look for the variable named `TITLE` and change the text inside the quotation marks to whatever you want your game to be called.

---

## Step 2: Understand How Settings are Loaded
**File to edit:** `main.py`
**Search for:** `@STUDENT-EDIT-Day1-2`

**Hint:** Notice the line right below this comment. It says `from settings import *`. This line is what allows `main.py` to use the `TITLE` variable you just created! Try running your game and see if your new title appears at the top of the window.
