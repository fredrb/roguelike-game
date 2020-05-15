import tcod as libtcod
from globals import GameStates

# TODO: Should have more explicit events
# Show inventory -> Toggle Inventory
# Exit -> Leave Game

def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn(key)
    if game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead(key)
    if game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    if game_state in (GameStates.INVENTORY, GameStates.DROP_INVENTORY):
        return handle_player_inventory(key)
    return {}

def handle_targeting_keys(key):
    if key == 27: # ESC
        return {'exit': True}
    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.tile[0], mouse.tile[1])

    if mouse.button == libtcod.event.BUTTON_LEFT:
        return {'left_click': (x, y)}
    if mouse.button == libtcod.event.BUTTON_RIGHT:
        return {'right_click': (x, y)}
    return {}

def handle_player_inventory(key):
    # TODO: Use esc
    if key == ord('i'):
        return {'show_inventory': True}
    if key == ord('o'):
        return {'drop_inventory': True}
    index = key - ord('a')
    if index >= 0:
        return {'inventory_index': index}
    return {}

    
def handle_player_dead(key):
    if key == ord('i'):
        return {'show_inventory': True}
    else:
        return {'exit': True}

def handle_player_turn(key):
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
    elif key == ord('g'):
        return {'pickup': True}
    elif key == ord('i'):
        return {'show_inventory': True}
    elif key == ord('o'):
        return {'drop_inventory': True}
    return {}
