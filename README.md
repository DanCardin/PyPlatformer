pyPlatformer
==========

## About
A 2D sidescrolling platforming engine.

Currently this is being developed alongside a generic game. At the moment, there isnt necessarily
much of a distinction between the engine and the game, but slowly game functionality is being moved
out into seperate files.

Random list of features:
- Parallax background scrolling
- Arbitrarily zoomable viewport onto the map
- NPCs (very basic AI (almost non-existent))
- Simple particle emitters (used for weapon firing and NPC spawns)

## Setup

## TODO:
### Engine vs Game
- Menus should probably be represented a in a flat file and loaded into the Game rather than
hardcoded into Game itself.
- MChar should be moved to game-space since Char is generic, but MChar is very specific to the
particular tileset and game
- Gravity currently is applied per-entity. This should really be a level attribute, and objects
should opt-in to being effected by gravity.

### add triggers/textual triggers 
- When colliding with this it will make some action happen.
- Textual trigger would be a bit of text that shows up on screen when a trigger is hit.

### sound
- Add sound effects on actions
- This could piggyback triggers, but also sounds associated with things like jumping would be ideal.

### Menus
- menus with keyboard input

### savestate
- Save and load gamestates

### More AI
- walk-Paths

### moving platforms
- Allow platforms (e.g. moving objects that allow something sitting on top of them (e.g. the player) to move with that object when it moves).

### slopes
- Each block would either:
    - be completely solid of a particular type (to save computation)
    - have 8 control points (4 for the corners, and 4 for halfway between each corner)
        + Two points per block can be connected form a line that will be the terrain for that block.
        + Then simply detect for collision with that line segment and appropriately push out depending on the type of collision.

### ledge grabbing and wall jumping
- The way its done in Stealth Bastard is really nice.
