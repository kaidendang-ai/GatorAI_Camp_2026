# Day 2: Sprites and Game Logic

## Objective
Explore game mechanics and make active changes to game code.

## Core Concepts

> **Ordering note:** Day 2 introduces the notebook's collection/style/library/function
> block **in the notebook's order: lists → naming/PEP8 → comments (revisit) → libraries →
> functions** (including tuples, `None`, positional args, defaults, and scope).
> **Libraries move here from Day 1** so the sequence matches the notebook. Conditionals
> and loops are camp-native (the notebook doesn't cover them) and stay woven into the
> game edits below.

- **Lists & zero-indexing** — sequences like `self.tools = ["hoe", "axe", "water"]`;
  `[0]` is the first element; lists can mix types
- **Naming & PEP8** — meaningful, legal, case-sensitive names
- **Comments (revisit)** — students wrote their first `#` comment on Day 1; today, comment
  the *why*, not the obvious
- **Libraries** — the three import styles, `help`/`dir`, and aliases
- **Functions** — read the player's methods, then **write your own** (`def`/docstring/
  `return`); tuples & unpacking, `None`, positional args, defaults, and scope
- **Loading Character Sprites** — import image files (PNGs) into game code, position them
- **Basic Conditionals** — `if`/`elif`/`else` and logical `or` for input (camp-native)

## Exercise: Adding Your First Character
The student-facing steps live in
[student_tutorials/Day2_Sprites.md](../../student_tutorials/Day2_Sprites.md).
- Add a custom NPC via the `NPC_DATA` dictionary in `settings.py`
- Use [Piskel](https://www.piskelapp.com/) to create unique sprites
- **Deliverable**: Push project to personal GitHub repository

## Code References

> Snippets are copied from the real project files. Search for the quoted code or the
> `@STUDENT-EDIT` marker rather than relying on exact line numbers.

### How Sprites Are Loaded From Folders
**File**: [support.py](../../support.py)

The whole game loads its animation frames with one small helper. This is a great first
look at functions, loops, and lists:

```python
from os import walk, path
import pygame

def import_folder(folder_path):
	surface_list = []
	base_path = path.dirname(path.abspath(__file__))

	for _, __, img_files in walk(path.join(base_path, folder_path)):
		for image in img_files:
			full_path = path.join(base_path, folder_path, image)
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list
```

**DETAILED WALKTHROUGH:**
1. **`def import_folder(folder_path):`** — a reusable function that takes a folder path
   and returns a *list* of loaded images.
2. **`surface_list = []`** — start with an empty list we will fill up.
3. **`for ... in walk(...)`** — `walk` visits the folder and gives back the file names.
   We use `_` and `__` for the parts we don't need (a common Python convention).
4. **`pygame.image.load(full_path).convert_alpha()`** — loads one image. `.convert_alpha()`
   keeps transparency and makes drawing faster.
5. **`surface_list.append(image_surf)`** — add the loaded image to our list.
6. **`return surface_list`** — hand back all the images. There is also an
   `import_folder_dict` here that returns a *dictionary* instead — a nice
   list-vs-dictionary comparison.

### The Player Sprite
**File**: [player.py](../../player.py) — `class Player`

The player is a `pygame.sprite.Sprite`. Its animations are stored in a dictionary and
filled by looping over folder names with the helper above:

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction,
                 soil_layer, toggle_shop, npc_sprites, trigger_dialogue, shake_camera):
        super().__init__(group)

        self.import_assets()  # Load all animation frames
        # @STUDENT-EDIT-Day2-3: Modify the player's starting direction
        self.status = "down_idle"  # Start facing down and not moving
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS["main"]

        self.speed = PLAYER_SPEED  # PLAYER_SPEED is defined in settings.py (@STUDENT-EDIT-Day2-2)
```

```python
    def import_assets(self):
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
            "right_hoe": [], "left_hoe": [], "up_hoe": [], "down_hoe": [],
            "right_axe": [], "left_axe": [], "up_axe": [], "down_axe": [],
            "right_water": [], "left_water": [], "up_water": [], "down_water": [],
            # @STUDENT-EDIT-Day5-2: Add custom animation folder path here
        }

        for animation in self.animations.keys():
            full_path = "graphics/character/" + animation
            self.animations[animation] = import_folder(full_path)
```

**DETAILED WALKTHROUGH:**
1. **`class Player(pygame.sprite.Sprite):`** — Player *inherits* from pygame's Sprite,
   which gives it built-in image/position handling.
2. **`self.import_assets()`** — loads every animation. Note there are separate
   animations for each tool (`hoe`, `axe`, `water`) and direction — this is a farming
   game, not a combat game.
3. **`self.status = "down_idle"`** — a *string* describing the current animation state.
   Marker `@STUDENT-EDIT-Day2-3` invites students to change the starting direction.
4. **`self.image` / `self.rect`** — the current picture and its position rectangle.
5. **`self.speed = PLAYER_SPEED`** — speed comes from `settings.py`. Marker
   `@STUDENT-EDIT-Day2-2` is where students tune it.
6. **`import_assets`** — builds a dictionary of empty lists, then a `for` loop fills
   each one by calling `import_folder`. This avoids writing 20 nearly-identical lines.

### Conditionals: Handling Input
**File**: [player.py](../../player.py) — `input()`

This method is the clearest example of `if`/`elif`/`else` driving behavior:

```python
    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["tool use"].active and not self.sleep:

            # MOVEMENT CONTROLS
            # @STUDENT-EDIT-Day2-5: Amend input controls to allow WASD movement using 'or'
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0
```

**DETAILED WALKTHROUGH:**
1. **`keys = pygame.key.get_pressed()`** — a snapshot of which keys are currently held.
2. **`if not self.timers["tool use"].active and not self.sleep:`** — a *guard*: we only
   accept movement input if the player isn't mid-swing and isn't sleeping. Good example
   of combining conditions with `and`/`not`.
3. **The `if/elif/else` blocks** set a direction value and an animation `status`.
   Marker `@STUDENT-EDIT-Day2-5` is where students add WASD by combining keys with
   `or`, e.g. `if keys[pygame.K_UP] or keys[pygame.K_w]:`.

### Functions Working Together: `move()`
**File**: [player.py](../../player.py) — `move()`

```python
    def move(self, dt):
        # Normalize so diagonal movement isn't faster than straight movement
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement + collision
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # Vertical movement + collision
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

        # @STUDENT-EDIT-Day2-4: Add a boundary check to keep the player on-screen
```

**DETAILED WALKTHROUGH:**
- **`dt`** is *delta time* (seconds since the last frame). Multiplying by `dt` makes
  movement speed the same on fast and slow computers.
- Horizontal and vertical movement are handled separately so the player can slide along
  walls — `self.collision(...)` is called after each.
- Marker `@STUDENT-EDIT-Day2-4` is the spot to add a simple boundary check (an `if`
  comparing `self.pos` to the screen size).

### Adding Your Own Character (Data-Driven NPCs)
**File**: [settings.py](../../settings.py) — `NPC_DATA`

Students do not need to write a new class to add a character. The game reads this
dictionary and spawns an NPC for each entry:

```python
# @STUDENT-EDIT-Day2-1: Add your custom sprite image name to the character list
NPC_DATA = {
    "Robin": {
        "pos": (800, 400),
        "graphic": "graphics/objects/merchant.png",  # Placeholder using existing asset
        "dialogue": [
            "Hi there! Welcome to Capitalism simulator!!",
            "I'm Robin, a helper NPC created using Python classes.",
            "Try editing settings.py to change what I say, or create your own custom NPC!"
        ]
    }
}
```

And in [level.py](../../level.py), `spawn_npcs()` loops over that dictionary:

```python
    def spawn_npcs(self):
        from sprites import NPC
        for npc_name, data in NPC_DATA.items():
            NPC(
                pos=data["pos"],
                surf=pygame.image.load(data["graphic"]).convert_alpha(),
                name=npc_name,
                dialogue=data["dialogue"],
                groups=[self.all_sprites, self.collision_sprites, self.npc_sprites]
            )
```

**DETAILED WALKTHROUGH:**
- `NPC_DATA` is a **dictionary of dictionaries**. Each key (`"Robin"`) maps to a
  position (a tuple), a graphic path (a string), and dialogue (a list of strings).
- `spawn_npcs()` uses a `for` loop and `.items()` to read each entry and build an `NPC`
  sprite. Adding `"Bella": {...}` to `NPC_DATA` is all a student needs to add a second
  character — a powerful demonstration of *data-driven design*.
- The `NPC` class itself is in [sprites.py](../../sprites.py) and is short — worth
  showing students that it just stores a name and dialogue on top of `Generic`.

### Lists and Zero-Indexing
**File**: [player.py](../../player.py) — `__init__`

Before the sprite work, point at a plain list students can reason about:

```python
self.tools = ["hoe", "axe", "water"]   # a list of three strings
self.tool_index = 0
self.selected_tool = self.tools[self.tool_index]   # self.tools[0] -> "hoe"
```

**DETAILED WALKTHROUGH:**
- A **list** is an ordered sequence in square brackets. Python is **zero-indexed**, so
  `self.tools[0]` is `"hoe"` and `self.tools[1]` is `"axe"`.
- Lists can even hold mixed types (`[1, 35, 5.6, "Fun"]`). Tie-in: in AI, lists organize
  *structure/config*, while NumPy arrays/tensors hold the actual *data* — the notebook
  notes lists are used less for large datasets.

### Naming and PEP8
**File**: [settings.py](../../settings.py) — `NPC_DATA`, marker `@STUDENT-EDIT-Day2-6`

Naming a new NPC key is a real chance to teach naming rules:

**DETAILED WALKTHROUGH:**
- Names use letters/digits/underscores, can't start with a digit, and should be
  meaningful. Python is **case-sensitive** (`Robin` ≠ `robin`).
- Illegal names (`1st_npc`, `my$npc`) raise a `SyntaxError` — and the `^` caret in the
  message points *near* the problem, sometimes a line above. PEP8 prefers
  `lower_case_with_underscores`. ML naming conventions (`X`, `y`, `w`, `b`) are a fun aside.

### Libraries (moved here from Day 1)
**File**: [main.py](../../main.py) — imports, marker `@STUDENT-EDIT-Day2-8`

Now the formal libraries lesson the notebook places *after* lists and naming:

```python
from settings import *          # everything from settings.py (use sparingly)
from main_menu import MainMenu   # one specific thing (a class)
import game_settings             # the whole module -> game_settings.load_settings()
# import game_settings as gs     # an alias, to type less
```

**DETAILED WALKTHROUGH:**
- A **library/module** is pre-written code you `import`. Contrast the three styles above,
  and the alias form. In a terminal, `help(pygame)` and `dir(math)` explore a library's
  contents. Tie-in: "coding for AI is mostly using libraries."

### Write Your Own Function
**File**: [support.py](../../support.py) — marker `@STUDENT-EDIT-Day2-7`

Students have *read* `import_folder`/`import_folder_dict`; now they write one from scratch:

```python
def add(x, y):
    '''Take two values and return their sum.'''
    return x + y
```

**DETAILED WALKTHROUGH:**
- A function has a `def` line (name + inputs), a **docstring**, indented body, and
  usually a `return`. **Defining** ≠ **calling**: `add(3, 4)` must be called to run.
  These are notebook Exercises 7 (define `add`), 8 (call it), and 9 (write `square`).

### Tuples, Arguments, and Scope
**File**: [scratch.py](../../scratch.py) — marker `@STUDENT-EDIT-Day2-9` (plus real tuples in
[settings.py](../../settings.py)'s `APPLE_POS`)

The notebook's function BONUS material has no game surface, so it lives in the playground:

```python
def powers(number):
    return number ** 2, number ** 3, number ** 4

values = powers(2)              # (4, 8, 16) -> a TUPLE
square, cube, fourth = powers(3)  # UNPACK into three names
```

**DETAILED WALKTHROUGH:**
- Returning several values packs them into a **tuple**; you can **unpack** into N names
  (a count mismatch errors). `APPLE_POS`'s `(x, y)` pairs are tuples too.
- **Positional arguments**: `describe(3, 4)` ≠ `describe(4, 3)` — order matters.
- **Default values**: an argument can have a default (`def add(x, y=1)`), used when the
  caller omits it — `add(2)` gives `3`, `add(2, 6)` gives `8`.
- A function with no `return` yields **`None`**. Variables made inside a function are
  **local** (gone once it returns) — reinforced again on Day 4.

## Key Learning Points
1. **Loading and displaying sprites** — `pygame.image.load`, `.convert_alpha()`, and
   organizing frames in a dictionary.
2. **Coordinate systems** — `(0, 0)` is top-left; `rect` vs `hitbox`.
3. **Conditionals respond to input** — `if/elif/else` over `pygame.key.get_pressed()`.
4. **Functions/methods organize logic** — `input()`, `move()`, `animate()` each do one
   job and are called from `update()`.
5. **Data-driven content** — adding a character by editing a dictionary, not code.
6. **Lists & zero-indexing** — `self.tools[0]`; lists can mix types.
7. **Naming & PEP8** — meaningful, legal, case-sensitive names.
8. **Libraries** — the three import styles, aliases, and `help`/`dir`.
9. **Writing functions** — `def`/docstring/`return`; tuples & unpacking, `None`,
   positional args, default values, and local scope.

## Extension Activities
1. **Add WASD movement** — `@STUDENT-EDIT-Day2-5` in `player.py` (use `or`).
2. **Keep the player on screen** — `@STUDENT-EDIT-Day2-4` in `move()`.
3. **Change starting direction** — `@STUDENT-EDIT-Day2-3` (`"down_idle"` → `"left_idle"`).
4. **Add a second NPC** — add an entry to `NPC_DATA` (`@STUDENT-EDIT-Day2-1`), naming the
   key well (`@STUDENT-EDIT-Day2-6`).
5. **Tune movement speed** — `PLAYER_SPEED` in `settings.py` (`@STUDENT-EDIT-Day2-2`).
6. **Write your own function** — `add`/`square` at `@STUDENT-EDIT-Day2-7` in `support.py`.
7. **Explore a library** — run `help(pygame)`/`dir(math)` (`@STUDENT-EDIT-Day2-8`).
8. **Play with tuples & arguments** — run `scratch.py` (`@STUDENT-EDIT-Day2-9`).

## Troubleshooting Tips
- **Sprite doesn't appear / `pygame.error: Couldn't open ...`:** the graphic path in
  `NPC_DATA` is wrong. Paths are relative to the project root, e.g.
  `graphics/objects/merchant.png`. Confirm the file exists.
- **`KeyError` on an animation:** the `status` string must match a folder under
  `graphics/character/` (e.g. `down_idle`). If you add a custom animation, also create
  the folder of frames.
- **Player moves too fast/slow or "teleports":** remember movement uses `dt`. Changing
  `PLAYER_SPEED` is the right knob; don't remove the `* dt`.
- **Diagonal movement feels faster:** that's why `move()` calls `.normalize()` — keep it.
