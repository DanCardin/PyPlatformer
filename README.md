pyPlatform
==========

## TODO: (In order of importance and doing)
### unformated ideas
- menus with keyboard input
- display char/enemy correctly at any resolution (preferably also menus, which i think are static)
- scale camera to work like a camera. difference between the correct size of camera (screenSize) and actual size translates to the zoom amount of all images.
	- ie. pygame.translate.scale(image, (camIdeal - camActual), dest image)
	- This might be easiest by: using an in-game unit of 1, then scaling from a scale,
	  caching the last image size from that scale to avoid scaling each frame, and finally dynamically changing scale.

### weapons
- make weapons actually kill things

### settings menu
- Allows customizable keys in-game
- Tabualar menus for stuff like "editor settings", "controls", etc

### damage
- Implement but not necessarily apply to mChar the idea of health.
- This is mostly for enemies to be hit by more than 1 bullet to die.

### sound
- Add sound effects on actions

### smarter npcs
- Spawn Points
- Paths
- fix inter object actions, for example bots dont correctly turn on different block types and die on bullet hits

### add triggers/textual triggers
- When colliding with this it will make some action happen.
- Textual trigger would basically just make a menu visible or invisible.

### savestate
- Save and load gamestates

### add ledge grabbing
- The way its done in Stealth Bastard is really nice.

### moving platforms
- Allow platform to move objects on it.
- Keep platforms from making objects stick to them
- Fix movement when on the platform so that it doesn't accelerate moving objects.

### slopes
- Not as necessary, but kind of cool.
- Would probably require a change in how objects that can move up slopes work.
- triangular points whose slope determines how steep a slope the char can move up.
