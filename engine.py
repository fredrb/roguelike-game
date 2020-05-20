import tcod as libtcod

from input_handlers import handle_keys, handle_mouse, handle_main_menu
from entity import Entity
from game_map import GameMap
from components.fighter import Fighter
from components.ai import BasicMonster
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from menu import inventory_menu, main_menu, message_box, level_up_menu, character_screen
from message_log import MessageLog, Message
from data_loaders import save_game

from graphics.render import Render
from graphics.scene.game import GameScene
from stage.main_menu import MainMenuStage

from globals import GameStates, RenderOrder, CONFIG


def component(name):
    # TODO: Change this into a proper factory
    component_map = {
        "PLAYER"    : Fighter(hp=60, defense=2, power=5),
        "ORC"       : Fighter(hp=10, defense=0, power=3, xp=35),
        "TROLL"     : Fighter(hp=16, defense=1, power=4, xp=100),
        "BASIC"     : BasicMonster(),
        "INVENTORY" : Inventory(26),
        "EQUIPMENT" : Equipment()
    }
    return component_map[name]


# TODO: Game context?
def get_game_variables():
    player = Entity(0, 0,
                    '@',
                    libtcod.black,
                    'Player',
                    True, 
                    render_order=RenderOrder.ACTOR, 
                    inventory=component("INVENTORY"),
                    equipment=component("EQUIPMENT"),
                    level=Level(),
                    fighter=component("PLAYER"))

    entities = [player]
    game_map = GameMap(CONFIG.get('MAP_WIDTH'), CONFIG.get('MAP_HEIGHT'))
    game_map.make_map(
        CONFIG.get('MAX_ROOMS'), 
        CONFIG.get('ROOM_MIN_SIZE'), 
        CONFIG.get('ROOM_MAX_SIZE'), 
        player, 
        entities, 
        CONFIG.get('MAX_MONSTERS'),
        CONFIG.get('MAX_ITEMS'),
        component)

    message_log = MessageLog(CONFIG.get("MESSAGE_X"),
                             CONFIG.get("MESSAGE_WIDTH"),
                             CONFIG.get("MESSAGE_HEIGHT"))

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state


def main():
    main_menu_stage = MainMenuStage()
    game_scene = GameScene()

    current_stage = main_menu_stage
    render = Render()

    render.start([
        main_menu_stage.scene,
        game_scene
    ])
    
    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    while True:
        key_pressed = None
        for event in libtcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()
            if event.type == "KEYDOWN":
                key_pressed = event.sym
        result = current_stage.run(key_pressed)
        if result.get('next_stage'):
            render.clear()
            player, entities, game_map, message_log, game_state = result.get('args')
            play_game(player, entities, game_map, message_log, game_state, game_scene)
        elif result.get('exit_game'):
            raise SystemExit()

class GameContextState:
    def __init__(self):
        self.error = None
        self.entities = []
        # TODO: change
        self.game_state = GameStates.PLAYERS_TURN
        self.previous_game_state = None
        self.message_log = None
        self.player = None
        self.targeting_item = None

def play_game(c_player, c_entities, c_game_map, c_message_log, c_game_state, scene):
    state = GameContextState()

    state.player = c_player
    state.entities = c_entities
    state.game_state = c_game_state
    state.game_map = c_game_map
    state.message_log = c_message_log

    while True:
        # TODO: Maybe there is an equivalent of Keymap as we have in SDL here?
        key_pressed = None
        mouse_moved = None
        mouse_clicked = None
        for event in libtcod.event.wait():
            #libtcod.console_flush()
            if event.type == "QUIT":
                raise SystemExit()
            if event.type == "KEYDOWN":
                key_pressed = event.sym
            if event.type == "MOUSEMOTION":
                mouse_moved = event
            if event.type == "MOUSEBUTTONDOWN":
                mouse_clicked = event

        scene.show(state)

        action = handle_keys(key_pressed, state.game_state) if key_pressed is not None else {}
        mouse_action = handle_mouse(mouse_clicked) if mouse_clicked is not None else {}
        player_turn_result = []

        exit = action.get('exit')
        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        drop_inventory = action.get('drop_inventory')
        targeting_cancelled = action.get('targeting_cancelled')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        if show_inventory:
            if state.game_state == GameStates.INVENTORY:
                state.game_state = state.previous_game_state
                redraw = True
            else:
                state.previous_game_state = state.game_state
                state.game_state = GameStates.INVENTORY

        if drop_inventory:
            if state.game_state == GameStates.DROP_INVENTORY:
                state.game_state = state.previous_game_state
                redraw = True
            else:
                state.previous_state_game = state.game_state
                state.game_state = GameStates.DROP_INVENTORY

        if show_character_screen:
            if state.game_state == GameStates.CHARACTER_SCREEN:
                state.game_state = state.previous_game_state
                redraw = True
            else:
                state.previous_game_state = state.game_state
                state.game_state = GameStates.CHARACTER_SCREEN

        if targeting_cancelled:
            state.game_state = state.previous_game_state
            state.message_log.add_message(Message('Targeting cancelled'))

        if inventory_index is not None and state.previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(state.player.inventory.items):
            item = state.player.inventory.items[inventory_index]
            if state.game_state == GameStates.INVENTORY:
                # TODO: Move fov_map to game_map
                player_turn_result.extend(state.player.inventory.use(item, entities=state.entities, fov_map=scene.fov_map))
            elif state.game_state == GameStates.DROP_INVENTORY:
                player_turn_result.extend(state.player.inventory.drop(item))

        if take_stairs and state.game_state == GameStates.PLAYERS_TURN:
            for entity in state.entities:
                if entity.stairs and entity.x == state.player.x and entity.y == state.player.y:
                    state.entities = state.game_map.next_floor(state.player, state.message_log, CONFIG, component)
                    # TODO: This should not be here
                    scene.fov_map = initialize_fov(state.game_map)
                    scene.fov_recompute = True
                    libtcod.console_clear(scene.owner.con)
                    break
            else:
                state.message_log.add_message(Message('No stairs found', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                state.player.fighter.base_max_hp += 20
                state.player.fighter.hp += 20
            elif level_up == 'str':
                state.player.fighter.base_power += 1
            elif level_up == 'agi':
                state.player.fighter.base_defense += 1
            state.game_state = state.previous_game_state
            
        if exit:
            print("Exit")
            if state.game_state in (GameStates.CHARACTER_SCREEN, GameStates.INVENTORY):
                state.game_state = state.previous_game_state
                redraw = True
            if state.game_state == GameStates.TARGETING:
                player_turn_result.append({'targeting_cancelled': True})
            else:
                save_game(state.player, state.entities, state.game_map, state.message_log, state.game_state)
                return True
       
        if move and state.game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            dest_x = state.player.x + dx
            dest_y = state.player.y + dy
            if not state.game_map.is_blocked(dest_x, dest_y):
                target = Entity.get_blocking(state.entities, dest_x, dest_y)
                if target:
                    attack_results = state.player.fighter.attack(target)
                    player_turn_result.extend(attack_results)
                else:
                    state.player.move(dx, dy)
                    scene.fov_recompute = True
                state.game_state = GameStates.ENEMY_TURN
        elif pickup and state.game_state == GameStates.PLAYERS_TURN:
            for entity in state.entities:
                if entity.item and entity.x == state.player.x and entity.y == state.player.y:
                    pickup_results = state.player.inventory.add_item(entity)
                    player_turn_result.extend(pickup_results)
                    break
            else:
                state.message_log.add_message(
                    Message('There is nothing here to pickup', libtcod.yellow)
                )

        if state.game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                item_use_results = state.player.inventory.use(state.targeting_item, entities=state.entities, fov_map=scene.fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_result.extend(item_use_results)
            elif right_click:
                player_turn_result.append({'targeting_cancelled': True})

        for result in player_turn_result:
            message = result.get('message')
            dead_entity = result.get('dead')
            item_added = result.get('item_added')
            item_consumed = result.get('consumed')
            item_dropped = result.get('item_dropped')
            equip = result.get('equip')
            targeting = result.get('targeting')
            targeting_cancelled = result.get('targeting_cancelled')
            xp = result.get('xp')
            if message:
                state.message_log.add_message(message)
            if dead_entity:
                if dead_entity == state.player:   
                    message, state.game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)
                state.message_log.add_message(message)
            if item_added:
                state.entities.remove(item_added)
                state.game_state = GameStates.ENEMY_TURN
            if item_consumed:
                state.game_state = GameStates.ENEMY_TURN
            if equip:
                equip_results = state.player.equipment.toggle_equip(equip)
                for equip_results in equip_results:
                    equipped = equip_results.get('equipped')
                    dequipped = equip_results.get('dequipped')
                    if equipped:
                        state.message_log.add_message(Message('Equipped %s' % equipped))
                    if dequipped:
                        state.message_log.add_message(Message('Dequipped %s' % dequipped))
                state.game_state = GameStates.ENEMY_TURN
            if item_dropped:
                state.entities.append(item_dropped)
                state.game_state = GameStates.ENEMY_TURN
            if targeting:
                state.previous_game_state = GameStates.PLAYERS_TURN
                state.game_state = GameStates.TARGETING
                state.targeting_item = targeting
                state.message_log.add_message(state.targeting_item.item.targeting_message)
            if targeting_cancelled:
                state.game_state = state.previous_game_state
                state.message_log.add_message(Message('Targeting Cancelled'))
            if xp:
                leveled_up = state.player.level.add_xp(xp)
                state.message_log.add_message(Message('You gain %s experience' % xp, libtcod.light_blue))
                if leveled_up:
                    state.message_log.add_message(Message(
                        'Your battle skills grow stronger! You reached level %s!' % state.player.level.current_level,
                        libtcod.yellow)
                    )
                    state.previous_game_state = state.game_state
                    state.game_state = GameStates.LEVEL_UP
        
        if state.game_state == GameStates.ENEMY_TURN:
            for entity in state.entities:
                if entity.ai:
                    enemy_turn_result = entity.ai.take_turn(state.player, scene.fov_map, state.game_map, state.entities)
                    for result in enemy_turn_result:
                        message = result.get('message')
                        dead_entity = result.get('dead')
                        if message:
                            state.message_log.add_message(message)
                        if dead_entity:
                            if dead_entity == state.player:   
                                message, state.game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)
                            state.message_log.add_message(message)
                            if state.game_state == GameStates.PLAYER_DEAD:
                                break
                    if state.game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                state.game_state = GameStates.PLAYERS_TURN

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
