# Cutest-Infernus

A tactical RPG game inspired by “Mewgenics” and many other from his genre but it’s so adorable that you wouldn’t even notice the pain and terror it exudes.

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
│   ├── 📁 Fonts/   # typography     
│   ├── 📁 Music/   # Music and sounds effects     
│   └── 📁 Sprites/ # All kind of tiles and sprites    
│
└── 📁 src/                 
    ├── 📁 Definitions/ 
    ├── 📁 Entities/ 
    ├── 📁 Models/         
    └── 📁 World/
    └── other Folders, just in case
```

* **Definitions:** It contains all the game's static rules, settings, and structures.
* **Entities:** It stores the characters' dynamic behavior and individual state machines (for example, walking or resting states), and in later stages it will contain the game's AI.
* **Models:** It contains the core functionality and data management of the systems, such as the logic and algorithms for creating the grid or procedural board, and the main abstract classes for the characters, along with the mathematical calculations behind their interactions.
* **World:** It controls the flow of the game and general world transitions or changes in conjunction with the global state stack and the classes that represent each game screen (Menu State, Battle State, Rest State, and Game Over). It is responsible for orchestrating the transition between these scenes.
