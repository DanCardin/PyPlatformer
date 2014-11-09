pyPlatform
==========

## Things Done:
- paralax background
- menus
- infinite scaling- map scrolling
- compositing
- map editor transparency
- multiple levels
- particle effects (gun)
- npc/npc spawning
- animation
- arbitrary gravity

## TODO:
### add triggers/textual triggers 
- When colliding with this it will make some action happen.
- Textual trigger would be a bit of text that shows up on screen when a trigger is hit.

### sound
- Add sound effects on actions
- This could piggyback triggers, but also sounds associated with things like jumping would be ideal.

### Menus
- menus with keyboard input
- Allows customizable keys in-game
- Tabualar menus for stuff like "editor settings", "controls", etc

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

### add ledge grabbing (absolute least thing I care about)
- The way its done in Stealth Bastard is really nice.
