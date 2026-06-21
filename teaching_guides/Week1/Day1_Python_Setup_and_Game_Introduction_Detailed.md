# Day 1: Python Setup and Game Introduction

## Objective
Set up programming environment and begin coding fundamentals.

## Setup Tasks
1. **Install & Run IDE**: Explain what IDEs are and set up development environment
2. **Install Python**: Walk through Python installation (if not already installed)
3. **GitHub Setup**: Sign-in or sign-up for GitHub account
4. **Download Project**: Clone from [Ian's GitHub Repository](https://github.com/UFResearchComputing/GatorAI_Camp_2026)
5. **Hello World**: Demonstrate running "Hello, World!" in a Python script

## Core Concepts
### Basic Python Syntax
- Simple print statements and comments
- Indentation rules in Python

### Libraries and Importing
- Explain how to import and use external libraries

### Game Environment Overview
- Introduce existing game framework
- Show game file locations and how to run the game

### Variables & Data Types (Basic)
- Integers, floats, strings
- Assign simple values (character names, positions, etc.)

## Exercise: Customize a Splash Screen
- Modify "Hello, World!" splash screen to display welcome message
- Use variables to store player name or game title
- **Deliverable**: Push project to personal GitHub repository

## Code References

### Main Entry Point
**File**: `main.py` (Lines 1-50)
- Shows the main game entry point
- Demonstrates module imports and installation
- Illustrates class structure and game initialization

```python
"""
PyDew Valley - Educational Game for Learning Python
==================================================
This is the main game file that starts and runs our farming simulation game.
Students will learn Python concepts through game development!

Educational Concepts Covered:
- Classes and Object-Oriented Programming
- Game loops and event handling
- Pygame library usage
- Module imports and organization
"""

# Import required modules for our game
from installer import install

# Install required packages if they're not already installed
install("pygame")  # Game development library
install("pytmx")  # Map loading library
install("kagglehub")  # Dataset library
install("requests")  # Library for web requests
install("opencv-python")  # Computer vision library
install("pytorch_lightning")
install("openai")  # AI API library for dialogue generation

import pygame  # Main game development library
import sys  # System operations
import os  # Operating system interface

# Import our custom game modules
from settings import *  # Game configuration settings
from level import Level  # Game world and gameplay
from main_menu import MainMenu  # Main menu system
from character_screen import CharacterScreen  # Player information screen
import game_settings  # Audio and game settings
from emotion_detector import EmotionDetector
from collections import deque
```

**DETAILED WALKTHROUGH:**
Let's examine each part of this code in detail to understand what it does and why it's important:

1. **Module Docstring (Lines 1-10)**:
   ```python
   """
   PyDew Valley - Educational Game for Learning Python
   ==================================================
   This is the main game file that starts and runs our farming simulation game.
   Students will learn Python concepts through game development!

   Educational Concepts Covered:
   - Classes and Object-Oriented Programming
   - Game loops and event handling
   - Pygame library usage
   - Module imports and organization
   """
   ```
   - This is a module-level docstring that explains what this file does
   - In Python, we use triple quotes (""") for docstrings that document modules, classes, and functions
   - Good docstrings follow conventions: they start with a capital letter, end with a period, and explain the purpose clearly
   - This helps other developers (and your future self) understand what this file is for without reading the code

2. **Custom Installer Function (Line 13)**:
   ```python
   from installer import install
   ```
   - This imports a custom function called `install` from our `installer.py` file
   - We created this function to simplify the process of checking if packages are installed and installing them if needed
   - This is an example of code reuse - we're using code we wrote in another file

3. **Dependency Installation (Lines 16-22)**:
   ```python
   # Install required packages if they're not already installed
   install("pygame")  # Game development library
   install("pytmx")  # Map loading library
   install("kagglehub")  # Dataset library
   install("requests")  # Library for web requests
   install("opencv-python")  # Computer vision library
   install("pytorch_lightning")
   install("openai")  # AI API library for dialogue generation
   ```
   - Each line calls our `install()` function with a different package name
   - The comments explain what each library is used for in our game
   - This ensures that when someone runs our game for the first time, all required dependencies are automatically installed
   - This is a common pattern in real-world applications to make setup easier for users

4. **Standard Library Imports (Lines 25-27)**:
   ```python
   import pygame  # Main game development library
   import sys  # System operations
   import os  # Operating system interface
   ```
   - These lines import modules that are part of Python's standard library
   - `pygame` is actually a third-party library, but we treat it like a standard import here since it's essential for our game
   - `sys` provides access to system-specific parameters and functions (like `sys.exit()`)
   - `os` allows interaction with the operating system (like checking if files exist or getting environment variables)
   - The comments explain what each module is used for

5. **Custom Module Imports (Lines 30-36)**:
   ```python
   # Import our custom game modules
   from settings import *  # Game configuration settings
   from level import Level  # Game world and gameplay
   from main_menu import MainMenu  # Main menu system
   from character_screen import CharacterScreen  # Player information screen
   import game_settings  # Audio and game settings
   from emotion_detector import EmotionDetector
   from collections import deque
   ```
   - These lines import code we've written ourselves for our game
   - `from settings import *` imports all variables from settings.py (we'll look at this file next)
   - `from level import Level` imports just the Level class from level.py
   - `import game_settings` imports the entire game_settings module so we can access it as `game_settings.something`
   - `from collections import deque` imports a specific data structure from Python's collections module
   - Notice we use different import styles depending on what we need:
     - `from module import *` when we want everything from a module (use sparingly!)
     - `from module import SpecificClass` when we just need one or two things
     - `import module` when we want to access multiple things from a module using dot notation

### Game Class Structure
**File**: `main.py` (Lines 50-100)
- Demonstrates the main Game class structure
- Shows how to initialize pygame and create game window
- Illustrates game state management

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

    Think of this as the "manager" that coordinates everything!
    """
    
    def __init__(self):
        # Initialize pygame modules
        pygame.init()
        
        # Create the game window with specified dimensions
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        # Set the window title
        pygame.display.set_caption(TITLE)
        
        # Create a clock object to control frame rate
        self.clock = pygame.time.Clock()
        
        # Initialize game state variables
        self.running = True
        # ...existing code...
```

**DETAILED WALKTHROUGH:**
Now let's examine our Game class in detail:

1. **Class Definition (Line 50)**:
   ```python
   class Game:
   ```
   - This defines a new class called `Game`
   - In object-oriented programming, a class is a blueprint for creating objects
   - Our Game class will contain all the logic for running our game

2. **Class Docstring (Lines 51-58)**:
   ```python
   """
   Main Game Class - The Heart of Our Game
   ======================================
   This class manages the entire game, including:
   - Starting up pygame and creating the game window
   - Managing the main menu and game screens
   - Running the main game loop
   - Handling user input and events

   Think of this as the "manager" that coordinates everything!
   """
   ```
   - Again, we use a docstring to explain what this class does
   - This helps developers understand the purpose of the class at a glance
   - Notice how we use ASCII art (`=======`) to create a visual separator - this is a common documentation practice

3. **Constructor Method (Line 60)**:
   ```python
   def __init__(self):
   ```
   - This is a special method called the constructor
   - It's automatically called when we create a new instance of the Game class (e.g., `game = Game()`)
   - The `__init__` method is where we initialize the object's state
   - The `self` parameter refers to the specific instance being created

4. **Pygame Initialization (Line 63)**:
   ```python
   # Initialize pygame modules
   pygame.init()
   ```
   - This initializes all the pygame modules we need for our game
   - It's crucial to call this before using any other pygame functions
   - Think of it as "turning on" the pygame engine

5. **Display Setup (Lines 66-67)**:
   ```python
   # Create the game window with specified dimensions
   self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
   
   # Set the window title
   pygame.display.set_caption(TITLE)
   ```
   - `pygame.display.set_mode((WIDTH, HEIGHT))` creates our game window
   - The dimensions come from constants defined in settings.py (WIDTH and HEIGHT)
   - We store the resulting display surface in `self.screen` so we can draw on it later
   - `pygame.display.set_caption(TITLE)` sets the text that appears in the window's title bar
   - TITLE is another constant imported from settings.py

6. **Clock Creation (Lines 70-71)**:
   ```python
   # Create a clock object to control frame rate
   self.clock = pygame.time.Clock()
   ```
   - This creates a Clock object that helps us control how fast our game runs
   - Without this, our game would run as fast as the computer can handle, which might be too fast
   - The clock ensures consistent gameplay across different hardware

7. **Game State Initialization (Line 74)**:
   ```python
   # Initialize game state variables
   self.running = True
   ```
   - We're setting up a flag to control our main game loop
   - When `self.running` is True, the game continues to run
   - When we set it to False (e.g., when the user closes the window), the game will exit
   - This is a common pattern in game development

## Key Learning Points
1. **Understanding how Python programs start execution**
   - The `if __name__ == "__main__":` pattern (though not shown here, it's used in the actual main.py)
   - How imports work and why we need them
   - The sequence of execution from top to bottom

2. **Working with modules and imports**
   - How to import built-in modules (sys, os)
   - How to import custom modules from our own files
   - How to use the `from installer import install` pattern for dependency management

3. **Basic class structure in Python**
   - How to define a class using the `class` keyword
   - The purpose of the `__init__` method (constructor)
   - How to use `self` to refer to instance variables and methods

4. **Initializing game libraries (pygame)**
   - Why we need to call `pygame.init()` before using pygame functions
   - How to create a display window with `pygame.display.set_mode()`
   - How to set window properties like title and icon

5. **Setting up game window and display**
   - Understanding the coordinate system in pygame (0,0 is top-left)
   - How to control frame rate with a Clock object
   - The importance of the game loop for continuous rendering

## Extension Activities
1. Modify the window title in main.py
   - Look for where `TITLE` is defined in settings.py
   - Change it to something personalized like "My Adventure Game"

2. Change the window size by adjusting WIDTH and HEIGHT constants
   - Find these constants in settings.py
   - Try different values like 1024x768 or 1920x1080
   - Note how larger sizes may affect performance

3. Add a simple print statement to see when the game starts
   - Add `print("Game starting!")` in the Game.__init__ method
   - Observe when this prints in the console

4. Experiment with different background colors
   - Look for where the screen is filled in the draw method
   - Try changing `WATER_COLOR` to different hex values like "#FF0000" (red)

## Troubleshooting Tips
- If pygame fails to install, check Python version compatibility
  - Make sure you're using Python 3.7 or higher
  - Try upgrading pip: `python -m pip install --upgrade pip`
- Ensure you're running commands in the correct directory
  - Your current directory should be the GatorAI_Camp_2026 folder
  - Use `pwd` (or `cd` in PowerShell) to verify your location
- Verify GitHub repository cloned successfully
  - Check that you can see all the files listed in the workspace structure
  - If missing, try cloning again: `git clone https://github.com/UFResearchComputing/GatorAI_Camp_2026`
- Check that all required files are present after cloning
  - Compare your folder to the workspace structure shown at the beginning
  - Pay special attention to .py files and asset folders like graphics/, audio/, etc.