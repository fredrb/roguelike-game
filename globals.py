from enum import Enum, auto
import tcod as libtcod

class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    INVENTORY = 4
    DROP_INVENTORY = 5
    TARGETING = 6
    LEVEL_UP = 7
    CHARACTER_SCREEN = 8
    SHOP = 9

class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()

class EquipmentSlots(Enum):
    MAIN_HAND = auto()
    OFF_HAND = auto()




CONFIG = {
    "WIDTH"             : 80,
    "HEIGHT"            : 50,
    "MAP_WIDTH"         : 80,
    "MAP_HEIGHT"        : 43,
    "TITLE"             : "Kenya Survival",

    # UI - HP Bar
    "BAR_WIDTH"         : 20,
    "PANEL_HEIGHT"      : 7,
    "PANEL_Y"           : 43, # height - panel_height

    # UI - Message Log
    # TODO: Find a way to compute these other than using hardcoded constants
    "MESSAGE_X"         : 22, # bar width +2
    "MESSAGE_WIDTH"     : 58, # width - bar_width - 2
    "MESSAGE_HEIGHT"    : 6, # panel_height - 1

    # Procedural Generation
    "ROOM_MAX_SIZE"     : 10,
    "ROOM_MIN_SIZE"     : 6,
    "MAX_ROOMS"         : 30,
    "MAX_MONSTERS"      : 3,
    "MAX_ITEMS"         : 2,

    # Render
    "FONT_PATH"              : "dejavu16x16_gs_tc.png",

    # Field of View
    "FOV_ALGORITHM"     : 1,
    "FOV_LIGHT_WALLS"   : True,
    "FOV_RADIUS"        : 10,

    "COLORS": {
        'dark_wall': libtcod.Color(18, 18, 20),
        'dark_ground': libtcod.Color(50, 50, 50),
        'light_wall': libtcod.Color(130, 130, 130),
        'light_ground': libtcod.Color(200, 200, 200),
        'black': libtcod.Color(0, 0, 0)
    }

}

