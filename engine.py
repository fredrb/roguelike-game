import tcod as libtcod

from input_handlers import handle_keys
from entity import Entity
from game_map import GameMap
from components.fighter import Fighter
from components.ai import BasicMonster
from message_log import MessageLog, Message

from globals import GameStates, RenderOrder, CONFIG

def component(name):
    # TODO: Change this into a proper factory
    component_map = {
        "PLAYER"    : Fighter(hp=30, defense=2, power=5),
        "ORC"       : Fighter(hp=10, defense=0, power=3),
        "TROLL"     : Fighter(hp=16, defense=1, power=4),
        "BASIC"     : BasicMonster()
    }
    return component_map[name]

def main():
    player = Entity(0, 0, '@', libtcod.black, 'Player', True, render_order=RenderOrder.ACTOR, fighter=component("PLAYER"))
    entities = [player]

    colors = {
        'dark_wall': libtcod.Color(18, 18, 20),
        'dark_ground': libtcod.Color(50, 50, 50),
        'light_wall': libtcod.Color(130, 130, 130),
        'light_ground': libtcod.Color(200, 200, 200)
    }

    libtcod.console_set_custom_font('arial10x10.png', 
        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    with libtcod.console_init_root(
        CONFIG.get('WIDTH'), CONFIG.get('HEIGHT'), CONFIG.get('TITLE'), False, None, 'C', True) as con:

        panel = libtcod.console_new(CONFIG.get('WIDTH'), CONFIG.get('PANEL_HEIGHT'))
        game_map = GameMap(CONFIG.get('MAP_WIDTH'), CONFIG.get('MAP_HEIGHT'))
        game_map.make_map(
            CONFIG.get('MAX_ROOMS'), 
            CONFIG.get('ROOM_MIN_SIZE'), 
            CONFIG.get('ROOM_MAX_SIZE'), 
            player, 
            entities, 
            CONFIG.get('MAX_MONSTERS'),
            component)

        fov_recompute = True
        fov_map = initialize_fov(game_map)

        message_log = MessageLog(CONFIG.get("MESSAGE_X"),
                                 CONFIG.get("MESSAGE_WIDTH"),
                                 CONFIG.get("MESSAGE_HEIGHT"))

        game_state = GameStates.PLAYERS_TURN

        while True:
            # TODO: Maybe there is an equivalent of Keymap as we have in SDL here?
            key_pressed = None
            mouse_clicked = None
            for event in libtcod.event.wait():
                #libtcod.console_flush()
                if event.type == "QUIT":
                    raise SystemExit()
                if event.type == "KEYDOWN":
                    key_pressed = event.sym
                if event.type == "MOUSEMOTION":
                    mouse_clicked = event

            if fov_recompute:
                recompute_fov(fov_map, player.x, player.y, CONFIG)

            render_all(con, panel, message_log, entities, player, game_map, fov_map,
                       fov_recompute,
                       CONFIG.get('WIDTH'),
                       CONFIG.get('HEIGHT'),
                       colors,
                       mouse_clicked)
            fov_compute = False
            libtcod.console_blit(con, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('HEIGHT'), 0, 0, 0)
            libtcod.console_flush()
            clear_all(con, entities)

            action = handle_keys(key_pressed)
            if action.get('exit'):
                return True

            player_turn_result = []

            move = action.get('move')
            if move and game_state == GameStates.PLAYERS_TURN:
                dx, dy = move
                dest_x = player.x + dx
                dest_y = player.y + dy
                if not game_map.is_blocked(dest_x, dest_y):
                    target = Entity.get_blocking(entities, dest_x, dest_y)
                    if target:
                        attack_results = player.fighter.attack(target)
                        player_turn_result.extend(attack_results)
                    else:
                        player.move(dx, dy)
                        fov_recompute = True
                    game_state = GameStates.ENEMY_TURN

            for result in player_turn_result:
                message = result.get('message')
                dead_entity = result.get('dead')
                if message:
                    message_log.add_message(message)
                if dead_entity:
                    if dead_entity == player:   
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_monster(dead_entity)
                    message_log.add_message(message)
            
            if game_state == GameStates.ENEMY_TURN:
                for entity in entities:
                    if entity.ai:
                        enemy_turn_result = entity.ai.take_turn(player, fov_map, game_map, entities)
                        for result in enemy_turn_result:
                            message = result.get('message')
                            dead_entity = result.get('dead')
                            if message:
                                message_log.add_message(message)
                            if dead_entity:
                                if dead_entity == player:   
                                    message, game_state = kill_player(dead_entity)
                                else:
                                    message = kill_monster(dead_entity)
                                message_log.add_message(message)
                                if game_state == GameStates.PLAYER_DEAD:
                                    break
                        if game_state == GameStates.PLAYER_DEAD:
                            break
                else:
                    game_state = GameStates.PLAYERS_TURN

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red
    return Message('You Died!', libtcod.red), GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = Message('%s is dead!' % monster.name.capitalize(), libtcod.orange)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message

def initialize_fov(game_map):
    fov_map = libtcod.map.Map(game_map.width, game_map.height)
    for y in range(game_map.height):
        for x in range(game_map.width):
            fov_map.transparent[y, x] = not game_map.tiles[x][y].block_sight
            fov_map.walkable[y, x] = not game_map.tiles[x][y].blocked
    return fov_map

def recompute_fov(fov_map, x, y, config):
    fov_map.compute_fov(
        x, 
        y, 
        config.get('FOV_RADIUS'), 
        config.get('FOV_LIGHT_WALLS'), 
        config.get('FOV_ALGORITHM'))

def clear_all(con, entities):
    for e in entities:
        libtcod.console_put_char(con, e.x, e.y, ' ', libtcod.BKGND_NONE)

def get_names_under_mouse(mouse_clicked, entities, fov_map):
    if not mouse_clicked:
        return []
    (x, y) = (mouse_clicked.tile[0], mouse_clicked.tile[1])
    names = [entity.name for entity in entities
            if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)
    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '%s: %i/%i' % (name, value, maximum))

def render_all(con, panel, message_log, entities, player, game_map, fov_map, fov_recompute, width, height, colors, mouse_clicked):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    for e in sorted(entities, key=lambda x: x.render_order.value):
        if libtcod.map_is_in_fov(fov_map, e.x, e.y):
            libtcod.console_set_default_foreground(con, e.color)
            libtcod.console_put_char(con, e.x, e.y, e.char, libtcod.BKGND_NONE)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, CONFIG.get('BAR_WIDTH'), 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)

    libtcod.console_set_default_foreground(panel, libtcod.gray)
    names = get_names_under_mouse(mouse_clicked, entities, fov_map)
    if len(names) > 0:
        libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, names)

    libtcod.console_blit(panel, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('PANEL_HEIGHT'), 0, 0, CONFIG.get('PANEL_Y'))

if  __name__ == '__main__':
    main()
