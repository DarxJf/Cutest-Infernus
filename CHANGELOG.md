# CHANGELOG

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

## [alpha v1.0.0] - 2026-09-18

### Added

- The definitions for entities, actions, and objects have been completed, so that more can be added in the future in a stable manner.
- The `Entity` model, responsible for placing entities on the grid; the `BattleEntity` class, which inherits from `Entity` to provide combat stats and actions performed by allies and enemies; and the class for managing equipable items. All classes safely handle the parameters of their definitions. They are also compatible with the factory pattern.
- The `CutestInfernus` game class has been set up as the entry point of the program. It creates a single `StateStack` and delegates `update`, `render`, and `on_input` to it, so every screen from here on lives on the stack instead of being managed ad hoc.
- The `settings` module now centralizes all constants the game needs: input bindings (`quit`, `moveLeft`, `moveRight`, `moveUp`, `moveDown`, `enter`, `pause`), virtual and window resolutions, the font registry, the texture and frame registries, the tile id map, the sound registry, and the save system configuration (`SAVE_DIR` and `SAVE_SLOTS`).
- A reusable `Menu` widget has been built on top of `gale.ui.ListView`. It handles cursor rendering, item navigation, confirmation, and the selection sound, so every screen that needs a menu (main menu, pause menu, confirm dialogs, slot selectors) can reuse it without duplicating layout code.
- The `StartState` has been added as the main menu of the game, offering `New game` and `Load game` options with keyboard navigation.
- The `SelectCharacterState` has been added so the player can pick the main character of the run with left/right navigation and confirm with Enter.
- The `PlayState` has been added as a placeholder for the active run. It exposes the pause menu through the `P` key and renders a minimal run-in-progress screen until later phases fill it with the board, party, and combat.
- The `PauseMenuState` has been added as an overlay on top of `PlayState`, offering `Continue`, `Save game`, `Load game`, and `Quit game`.
- The `SlotSelectState` has been added to let the player pick one of the three save slots in either `save` or `load` mode. It lays out one card per slot, highlights the selected one, and supports cancel with `P`.
- The `GameOverState` has been added as the end-of-run screen. Confirming with Enter clears the entire state stack and pushes a fresh `StartState`, so the discarded run cannot be recovered.
- The `FadeInState` and `FadeOutState` have been added for full-screen color transitions. Both run a `Timer` tween over the requested duration and call an `onComplete` callback once the tween finishes, so callers can swap scenes at the blind spot of the transition.
- The `MovementCalculator` for player and ai is complete.
- Glow effect for avaivable movement.
- The `Room` model has been added. It procedurally generates a battle arena on a grid.
- Rocks have been added as solid obstacles in the `Room`.
- Torches have been added as decorative objects.
- Compute damage to `hurt` or `heal`, it improves with affinity stats of the action.
- AoE Logic for actions. Also, for single target.
- AoE Logic implemented well in `BattleState`, therefore rules of the battle, movement with bfs, etc.
- Menu for select action, movement, strike or end turn workly in `BattleState` render by `batleUI`.
- Cooldowns for actions and effects status, like stunned or poisoned in `BatttleState`.
- The rest area is now playable as a hub between battles. `RestState` shows a menu for `Hire companion`, `Shop`, `Inventory`, `Manage actions`, and `Leave`. `HireState` offers a random rotating pool of secondary characters each visit; `ShopState` sells passive objects; `InventoryState` handles equipping into each member's slots.
- `RunState` bundles everything that lives for the duration of a run the `Party`, the shared `Inventory`, the `RunWallet` (mutable soul count), the current `RestOffers`, and the boss progression counters so states can receive a single `runState` argument and mutations propagate by reference.
- `IA` workly with a behavior tree. `IA` could move and attack nearest `Party` target. Each `Enemy` has it's own brain to do actions.
- `Animations` included on game. Each entity have it's current state like `IdleState`, `WalkState`, `AttackState` with tweens to allow animations for every state.
- `ActionInfoPanel` helps the player to know about character's abilities, is include in `BattleState` and `ManageActions`
- Functions on settings to play and stop music. Main theme made by us.
- `RestOffers` and `ShopOffers` manage the rotating offers.
- `TurnQueue` drives the battle in rounds. At the start of each round it sorts every living entity by agility (highest first, stable tie-break), and that order stays fixed until the round is over. The HUD shows the current actor plus a preview of the next turns, and dead entities are skipped without rebuilding the round.
- `EncounterGenerator` builds the enemy horde by scaling both the pool of available types and the level bonus with `battlesFought`. A separate `generate_boss_encounter` builds a boss plus two minions, scaling the boss further with `bossesDefeated`.
- Save / load through `gale.save.SaveManager`.
