import tcod as libtcod

from graphics.render import Render
from stage.main_menu import MainMenuStage
from stage.game import GameStage
from stage.city import CityMenuStage

def main():
    stages = {
        'main_menu': MainMenuStage(),
        'city': CityMenuStage(),
        'game': GameStage()
    }

    current_stage = stages.get('main_menu')
    render = Render()

    render.start([
        stages.get('main_menu').scene,
        stages.get('city').scene,
        stages.get('game').scene
    ])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    while True:
        key_pressed = None
        mouse_moved = None
        mouse_clicked = None
        next_stage = None
        for event in libtcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
            if event.type == "KEYDOWN":
                key_pressed = event.sym
            if event.type == "MOUSEMOTION":
                mouse_moved = event
            if event.type == "MOUSEBUTTONDOWN":
                mouse_clicked = event
        result = current_stage.run((key_pressed, mouse_moved, mouse_clicked))
        next_stage = result.get('next_stage')
        if next_stage is not None:
            render.clear()
            args = result.get('args')
            current_stage = stages.get(next_stage)
            if args:
                current_stage.load(args)
        elif result.get('exit_game'):
            raise SystemExit()

def get_names_under_mouse(mouse_moved, entities, fov_map):
    if not mouse_moved:
        return []
    (x, y) = (mouse_moved.tile[0], mouse_moved.tile[1])
    names = [entity.name for entity in entities
            if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)
    return names.capitalize()

if  __name__ == '__main__':
    main()
