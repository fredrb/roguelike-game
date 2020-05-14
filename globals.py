from enum import Enum

class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

CONFIG = {
    "WIDTH"             : 80,
    "HEIGHT"            : 50,
    "MAP_WIDTH"         : 80,
    "MAP_HEIGHT"        : 43,
    "TITLE"             : "Example Roguelike Game",

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

    # Field of View
    "FOV_ALGORITHM"     : 1,
    "FOV_LIGHT_WALLS"   : True,
    "FOV_RADIUS"        : 10
}

