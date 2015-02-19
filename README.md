pyPlatformer
==========

## About
A 2D sidescrolling platforming engine.

At the moment, there isnt necessarily much of a distinction between the engine and the game inside of it, but slowly game functionality is being moved out.

Random list of features:
- Parallax background scrolling
- Arbitrarily zoomable viewport into the level 
- Simple particle emitters (used for weapon firing and NPC spawns)
- NPCs (very basic AI (almost non-existent))

## Setup

## TODO:
### Cleanup of existing things
- Menu attriubutes should be represented a in a flat file and loaded rather than being hardcoded into Game itself.
- MChar specification sould be factored out. Its essentially a Char with specific settings.
- Gravity is currently an entity attribute. This should really be a level attribute, and objects should opt-in to being affected by gravity.
- Objects sitting on top of one another should move with that the object its sitting on top of. Get this working for current Enemy objects, and you've got free moving platforms.
- tilesets are just tuples and are adhoc loaded at the moment. A `Tileset` should be an object that manages loading, keeps track of size and whatnot
- backgrounds
    - should be map attributes not loaded in the level
    - probably be genericized to be an array of `Tileset`s with only 1 tile that's the size of the background. This would (hopefully) allow for lazy loading for really really big maps.

### Add triggers
- An object with whom objects can register in order to trigger some event. This is already someone done through the event system, but its not generic enough to be aribitrarily used for triggering events.

### Sound
- Add a sound engine with which other objects can register to play sounds. I was thinking this might work well using a decorator that wraps relevent events or method calls (like a jump method).

### Menus
- menus with keyboard input, there's no technical limitation to this really, i just cant immediately think of a clean way to specify connections between menu items for good movement. Maybe {keyEvent: nextButton} per button?

### Savestate
- clean way of serialising gamestate.
    - maybe objects inherit from Serializable and on __serialise__ we gather state from Game which traverses down through all contained objects and return it. Then the reverse for __deserialise__. A good solution would only require each object to specify *what* their state is and not require manual loading and saving for each piece.

### Slopes
- Each block would either:
    - be completely solid of a particular type (to save computation)
    - have 8 control points (4 for the corners, and 4 for halfway between each corner)
        + Two points per block can be connected form a line that will be the terrain for that block.
        + Then simply detect for collision with that line segment and appropriately push out depending on the type of collision.

### More AI
- Pathing
- Goals (follow players, shoot at players, etc)
- Line of site or radius of awareness
