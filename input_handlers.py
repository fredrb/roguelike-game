import tcod as libtcod

def handle_keys(key):
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
    return {}
