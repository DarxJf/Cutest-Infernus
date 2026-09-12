# CHANGELOG

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

### Added

- The definitions for entities, actions, and objects have been completed, so that more can be added in the future in a stable manner.
- The `Entity` model, responsible for placing entities on the grid; the `BattleEntity` class, which inherits from `Entity` to provide combat stats and actions performed by allies and enemies; and the class for managing equipable items. All classes safely handle the parameters of their definitions. They are also compatible with the factory pattern.
