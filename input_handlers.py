import tcod as libtcod
from globals import GameStates, CONFIG 

def handle_main_menu(key):
    if key == ord('1'):
        return {'new_game': True}
    if key == ord('2'):
        return {'exit': True}
    return {}

def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn(key)
    if game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead(key)
    if game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    if game_state == GameStates.SHOP:
        return handle_shop(key)
    if game_state == GameStates.INSTRUCTIONS:
        if key is not None:
            return {'exit_instructions': True}
    return {}

def handle_shop(key):
    if key == 27:
        return {'exit': True}
    index = key - ord('1')
    if index >= 0:
        return {'shop_index': index}
    return {}

def handle_targeting_keys(key):
    if key == 27: # ESC
        return {'exit': True}
    return {}

def handle_mouse_move(mouse):
    (x, y) = (mouse.tile[0], mouse.tile[1])
    return (x, y)

def handle_mouse(mouse):
    (x, y) = (mouse.tile[0], mouse.tile[1])

    if mouse.button == libtcod.event.BUTTON_LEFT:
        return {'left_click': (x, y)}
    if mouse.button == libtcod.event.BUTTON_RIGHT:
        return {'right_click': (x, y)}
    return {}

def handle_player_dead(key):
    #if key == ord('r'):
    #    return {'replay': True}
    if key == 27:
        return {'exit': True}
    else:
        return {}

def handle_player_turn(key):
    if key:
        print('Key: %i' % key)
    if key == ord('w'):
        return {'move': (0, -1)}
    elif key == ord('s'):
        return {'move': (0, 1)}
    elif key == ord('a'):
        return {'move': (-1, 0)}
    elif key == ord('d'):
        return {'move': (1, 0)}
    elif key == ord('q'):
        return {'move': (-1, -1)}
    elif key == ord('e'):
        return {'move': (1, -1)}
    elif key == ord('z'):
        return {'move': (-1, 1)}
    elif key == ord('c'):
        return {'move': (1, 1)}
    # elif key == ord('v'):
    #    return {'debug_take_stairs': True}
    elif key == 32: # space
        return {'take_stairs': True}
    elif key == 13:
        return {'take_stairs': True}
    elif key == 27:
        return {'exit': True}
    elif key == 47: # ?
        return {'show_help': True}
    elif key in (ord('1'), ord('2'), ord('3'), ord('4')):
        return {'hotkey': chr(key)}
    return {}
