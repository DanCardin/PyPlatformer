pyPlatform
==========

## TODO: (In order of importance and doing)
### unformated ideas
- menus with keyboard input

### Viewport
- display char/enemy correctly at any resolution (preferably also menus, which i think are static)
- scale camera to work like a camera. difference between the correct size of camera (screenSize) and actual size translates to the zoom amount of all images.
	- ie. pygame.translate.scale(image, (camIdeal - camActual), dest image)
	- This might be easiest by: using an in-game unit of 1, then scaling from a scale,
	  caching the last image size from that scale to avoid scaling each frame, and finally dynamically changing scale.

### damage
- Implement the idea of health and damage.
- This is mostly for enemies to be hit by more than 1 bullet to die.

### npcs
- Spawn Points (Potentially by generic-ing the particle emitting class)
- walk-Paths

### add triggers/textual triggers 
- When colliding with this it will make some action happen.
- Textual trigger would be a bit of text that shows up on screen when a trigger is hit.

### sound
- Add sound effects on actions
- This could piggyback triggers, but also sounds associated with things like jumping would be ideal.

### savestate
- Save and load gamestates

### moving platforms
- Allow platforms (e.g. moving objects that allow something sitting on top of them (e.g. the player) to move with that object when it moves).

### slopes
- Each block would either:
    - be completely solid of a particular type (to save computation)
    - have 8 control points (4 for the corners, and 4 for halfway between each corner)
        + Two points per block can be connected form a line that will be the terrain for that block.
        + Then simply detect for collision with that line segment and appropriately push out depending on the type of collision.

### settings menu
- Allows customizable keys in-game
- Tabualar menus for stuff like "editor settings", "controls", etc

### add ledge grabbing (absolute least thing I care about)
- The way its done in Stealth Bastard is really nice.
