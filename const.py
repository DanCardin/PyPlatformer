res = 32
PLAYER_NUM = 1
TILE_SET_LENGTH = 20

gameName = "Story of a Square"
levelFiles = [("assets\\level1.txt", "assets\\tileset3.bmp", 16),
              ("assets\\level2.txt", "assets\\tileset3.bmp", 16)]
playerTileset = "assets\\2run.bmp"
settings = "assets\\settings.txt"
screenSize = (20, 17)
FPS = 30
playerSpeed = (3, 8)
currLevel = 0

backgrounds = [
((480, 320), 4, "assets\\background.png"),
((480, 320), 2, "assets\\background2.png"),
((480, 320), 0, "assets\\background3.png")
]
