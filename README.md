# Cutest-Infernus

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
![Gale](https://img.shields.io/badge/Gale-1.17.0-6C5CE7)

A tactical RPG game inspired by “Mewgenics” and many other from his genre but it’s so adorable that you wouldn’t even notice the pain and terror it exudes.

The supreme god of your world has trapped you in a black hole that has swallowed everything you've ever known. But you're still alive! In this tactical role-playing game, which incorporates some roguelike mechanics, you'll have to venture into dungeons and defeat hordes of enemies, hire mercenaries, buy items, and lead a party of four members with unique powers to get as far as possible.

## How to execute

First of all, make sure you have the Gale engine installed. It is recommended to create and activate a virtual environment first.

### Linux and macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
python -m venv venv
venv\Scripts\activate.bat
```

To leave the virtual environment on any platform:

```bash
deactivate
```

### Gale Engine by pip

```bash
pip install gale-engine
```

---

Then you have everything, just go to the root project (Don't enter into any carpet) and write:

```bash
python3 main.py
```

or

```bash
python3.x main.py
```

The `x` represent the version of python installed on your computer.

## Structure Rules

### Archive Names

All archives `.py` have to be written in `PascalCase` except `settings.py` and `main.py`.

### Code Rules

To ensure readability, teamwork, and easy understanding of the code, these will be the coding standards:

* **Classes:** Written in `PascalCase`.

```Python
class Mage():
    pass

class BoardGenerator():
    pass
```

* **Variables and Class Attributes:** Written in `camelCase`.

```Python
magicDefense: int = 2

somethingElseYeah = True
```

* **Functions and Methods:** Written in `snake_case`.

```Python
def calculate_damage():
    pass
```

* If an archive has a method that is only use there, it will begin with `_`.

```Python
def _only_here():
    pass
```

---

### Order for importations

To avoid confusion and circular dependencies, imports at the beginning of each `.py` file should be grouped with a blank line between each group, in this exact order:

1. **Standard Python libraries** (e.g., `import random`, `import math`).
2. **External libraries** (e.g., `import gale`, `import pygame`).
3. **Internal code modules** (e.g., `from src.Models.entity import Entity`).

```Python
import random

from gale.timer import Timer

from src.Models.Entity import Entity
```

---

### Folder Structure

The following structure may change in the future:

```text
📁 Raíz del Proyecto
├── 📁 assets/  # Multimedia resources
│   ├── 📁 Fonts/  # Typography
│   ├── 📁 Music/  # Music and sound effects
│   └── 📁 Sprites/  # All kinds of tiles and sprites
│       ├── 📁 Entities/
│       │   ├── 📁 Characters/
│       │   └── 📁 Enemies/
│       │       ├── 📁 Boss/
│       │       ├── 📁 Demon/
│       │       │   ├── 📁 Idle/
│       │       │   └── 📁 Walk/
│       │       ├── 📁 Skeleton/
│       │       │   ├── 📁 Idle/
│       │       │   └── 📁 Walk/
│       │       └── 📁 Slime/
│       ├── 📁 Objects/
│       └── 📁 Rooms/
|
├── 📁 saves/
├── 📁 src/
    ├── 📁 ai/
    ├── 📁 Animations/
    ├── 📁 Definitions/
    ├── 📁 Gui/
    ├── 📁 Models/
    ├── 📁 States/
    │   ├── 📁 Entity/
    │   └── 📁 Game/
    └── 📁 Utils/
```

* **Definitions:** It contains all the game's static rules, settings, and structures.
* **ai:** It contains the behavior logic used by enemies during battles.
* **Animations:** It contains entity animation and tweening logic.
* **Gui:** It contains the game's user interface screens and panels.
* **Models:** It contains the core functionality and data management of the systems, such as the logic and algorithms for creating the grid or procedural board, and the main abstract classes for the characters, along with the mathematical calculations behind their interactions.
* **States:** It controls the flow of the game and general world transitions in conjunction with the global state stack. It includes entity states and game states such as Menu, Battle, Rest, and Game Over.
* **Utils:** It contains reusable calculations and helpers used by the game's systems.
