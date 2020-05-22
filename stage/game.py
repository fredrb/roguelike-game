import tcod
from graphics.scene.game import GameScene
from globals import GameStates, CONFIG, RenderOrder
from input_handlers import handle_keys, handle_mouse, handle_mouse_move
from message_log import Message
from components.factory import component
from entity import Entity

class GameInputHandler:
    def on_key(self, key, state):
        return handle_keys(key, state.game_state)

class GameState():
    def __init__(self):
        self.loaded = False
        self.error = None
        self.game_map = None
        self.entities = []
        # TODO: change
        self.game_state = GameStates.PLAYERS_TURN
        self.previous_game_state = None
        self.message_log = None
        self.player = None
        self.targeting_item = None
        self.targeting_index = None
        self.mouse_x = 0
        self.mouse_y = 0

class GameAct():
    def __init__(self, scene):
        # TODO: Shouldn't have, but keeping here for convenience now
        self.scene = scene

    def perform(self, state, action, mouse_action, mouse_move):
        player_turn_result = []

        exit = action.get('exit')
        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        shop_index = action.get('shop_index')
        take_stairs = action.get('take_stairs')
        drop_inventory = action.get('drop_inventory')
        targeting_cancelled = action.get('targeting_cancelled')
        level_up = action.get('level_up')
        hotkey = action.get('hotkey')
        show_character_screen = action.get('show_character_screen')
        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')
        (mouse_x, mouse_y) = mouse_move

        if show_inventory:
            if state.game_state == GameStates.INVENTORY:
                state.game_state = state.previous_game_state
                #redraw = True
            else:
                state.previous_game_state = state.game_state
                state.game_state = GameStates.INVENTORY

        if drop_inventory:
            if state.game_state == GameStates.DROP_INVENTORY:
                state.game_state = state.previous_game_state
                #redraw = True
            else:
                state.previous_state_game = state.game_state
                state.game_state = GameStates.DROP_INVENTORY

        if show_character_screen:
            if state.game_state == GameStates.CHARACTER_SCREEN:
                state.game_state = state.previous_game_state
                #redraw = True
            else:
                state.previous_game_state = state.game_state
                state.game_state = GameStates.CHARACTER_SCREEN

        if targeting_cancelled:
            state.game_state = state.previous_game_state
            state.message_log.add_message(Message('Targeting cancelled'))

        if shop_index is not None and shop_index < len(state.game_map.shopkeeper.shop.options):
            tome = state.game_map.shopkeeper.shop.options[shop_index]
            player_turn_result.extend(tome.use(state.player))
             

        if inventory_index is not None and state.previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(state.player.inventory.items):
            item = state.player.inventory.items[inventory_index]
            if state.game_state == GameStates.INVENTORY:
                # TODO: Move fov_map to game_map
                player_turn_result.extend(state.player.inventory.use(item, entities=state.entities, fov_map=self.scene.fov_map))
            elif state.game_state == GameStates.DROP_INVENTORY:
                player_turn_result.extend(state.player.inventory.drop(item))

        if take_stairs and state.game_state == GameStates.PLAYERS_TURN:
            for entity in state.entities:
                if entity.stairs and entity.x == state.player.x and entity.y == state.player.y:
                    state.entities = state.game_map.next_floor(state.player, state.message_log, CONFIG, component)
                    # TODO: This should not be here
                    self.scene.fov_map = GameScene.init_fov_map(state.game_map)
                    self.scene.fov_recompute = True
                    tcod.console_clear(self.scene.owner.con)
                    break
            else:
                state.message_log.add_message(Message('No stairs found', tcod.yellow))
            
        if exit:
            if state.game_state in (GameStates.CHARACTER_SCREEN, GameStates.INVENTORY):
                state.game_state = state.previous_game_state
                redraw = True
            elif state.game_state == GameStates.SHOP:
                state.game_state = GameStates.ENEMY_TURN
            elif state.game_state == GameStates.TARGETING:
                player_turn_result.append({'targeting_cancelled': True})
            else:
                # TODO: Port save
                #save_game(state.player, state.entities, state.game_map, state.message_log, state.game_state)
                player_turn_result.append({'exit_game': True})

        if hotkey and state.game_state == GameStates.PLAYERS_TURN:
            results = state.player.inventory.use_hotkey(int(hotkey), entities=state.entities, fov_map=self.scene.fov_map)
            player_turn_result.extend(results)
       
        if move and state.game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            dest_x = state.player.x + dx
            dest_y = state.player.y + dy
            if not state.game_map.is_blocked(dest_x, dest_y):
                target = Entity.get_blocking(state.entities, dest_x, dest_y)
                if target:
                    if target.shop:
                        player_turn_result.append({'open_shop': True})
                    elif target.container:  
                        open_results = target.container.open(state.player)
                        player_turn_result.extend(open_results)
                    elif target.item:
                        pickup_results = state.player.inventory.add_item(target)
                        player_turn_result.extend(pickup_results)
                    else:
                        attack_results = state.player.fighter.attack(target)
                        player_turn_result.extend(attack_results)
                else:
                    state.player.move(dx, dy)
                    self.scene.fov_recompute = True
                state.game_state = GameStates.ENEMY_TURN
        elif pickup and state.game_state == GameStates.PLAYERS_TURN:
            for entity in state.entities:
                if entity.item and entity.x == state.player.x and entity.y == state.player.y:
                    pickup_results = state.player.inventory.add_item(entity)
                    player_turn_result.extend(pickup_results)
                    break
            else:
                state.message_log.add_message(
                    Message('There is nothing here to pickup', tcod.yellow)
                )

        if state.game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                item_use_results = state.player.inventory.use_hotkey(state.targeting_index, entities=state.entities, fov_map=self.scene.fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_result.extend(item_use_results)
            elif right_click:
                player_turn_result.append({'targeting_cancelled': True})
            self.scene.fov_recompute = True

        return player_turn_result

class GameAiAct:
    def __init__(self, scene):
        self.scene = scene

    def perform(self, state):
        for entity in state.entities:
            if entity.ai:
                enemy_turn_result = entity.ai.take_turn(state.player, self.scene.fov_map, state.game_map, state.entities)
                for result in enemy_turn_result:
                    message = result.get('message')
                    dead_entity = result.get('dead')
                    if message:
                        state.message_log.add_message(message)
                    if dead_entity:
                        if dead_entity == state.player:   
                            message, state.game_state = GameAiAct.kill_player(dead_entity)
                        else:
                            message = GameAiAct.kill_monster(dead_entity)
                        state.message_log.add_message(message)
                        if state.game_state == GameStates.PLAYER_DEAD:
                            break
                if state.game_state == GameStates.PLAYER_DEAD:
                    break
        else:
            state.game_state = GameStates.PLAYERS_TURN

    @staticmethod
    def kill_player(player):
        player.char = '%'
        player.color = tcod.dark_red
        return Message('You Died!', tcod.red), GameStates.PLAYER_DEAD

    @staticmethod
    def kill_monster(monster):
        death_message = Message('%s is dead!' % monster.name.capitalize(), tcod.orange)
        monster.char = '%'
        monster.color = tcod.dark_red
        monster.blocks = False
        monster.fighter = None
        monster.ai = None
        monster.name = 'remains of ' + monster.name
        monster.render_order = RenderOrder.CORPSE

        return death_message

class GameStateReporter:
    def update(self, state, results):
        for result in results:
            print("Processing result %s" % result)
            message = result.get('message')
            dead_entity = result.get('dead')
            item_added = result.get('item_added')
            item_consumed = result.get('consumed')
            item_dropped = result.get('item_dropped')
            equip = result.get('equip')
            targeting = result.get('targeting')
            targeting_index = result.get('targeting_index')
            targeting_cancelled = result.get('targeting_cancelled')
            exit_game = result.get('exit_game')
            open_shop = result.get('open_shop')
            container_consumed = result.get('container_consumed')
            loot = result.get('loot')
            if exit_game:
                return {'exit_game': True}
            if message:
                state.message_log.add_message(message)
            if dead_entity:
                if dead_entity == state.player:   
                    message, state.game_state = GameAiAct.kill_player(dead_entity)
                else:
                    message = GameAiAct.kill_monster(dead_entity)
                state.message_log.add_message(message)
            if item_added:
                state.entities.remove(item_added)
                state.game_state = GameStates.ENEMY_TURN
            if container_consumed:
                state.entities.remove(container_consumed)
                state.game_state = GameStates.ENEMY_TURN
            if loot:
                message = state.player.purse.add_coins(loot) 
                #state.message_log.add_message(message)
            if item_consumed:
                state.game_state = GameStates.ENEMY_TURN
            if open_shop:
                state.game_state = GameStates.SHOP
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
            if targeting_index:
                state.targeting_index = targeting_index
            if targeting_cancelled:
                state.game_state = state.previous_game_state
                state.message_log.add_message(Message('Targeting Cancelled'))
        return {}

class GameStage:
    def __init__(self):
        self.scene = GameScene()
        self.input_handler = handle_keys
        self.mouse_move_handler = handle_mouse_move
        self.mouse_click_handler = handle_mouse
        self.act = GameAct(self.scene)
        self.ai_act = GameAiAct(self.scene)
        self.state = GameState()
        self.reporter = GameStateReporter()
        self.name = "Game"

        self.last_x, self.last_y = (0, 0)

    def load(self, args):
        player, entities, game_map, message_log, game_state = args
        self.state.loaded = True
        self.state.player = player
        self.state.entities = entities
        self.state.game_map = game_map
        self.state.message_log = message_log
        self.state.game_state = game_state

    def run(self, events):
        key, mouse_move, mouse_click = events
        if not self.state.loaded:
            raise SystemError("Stage ran before state was loaded")
        self.scene.show(self.state)

        action = self.input_handler(key, self.state.game_state) if key is not None else {}
        action_mouse_click = self.mouse_click_handler(mouse_click) if mouse_click is not None else {}

        if mouse_move:
            self.last_x, self.last_y = self.mouse_move_handler(mouse_move)
        self.state.mouse_x = self.last_x
        self.state.mouse_y = self.last_y
        action_mouse_move = (self.last_x, self.last_y)

        results = self.act.perform(self.state, action, action_mouse_click, action_mouse_move)
        external_events = self.reporter.update(self.state, results)

        if self.state.game_state == GameStates.ENEMY_TURN:
            self.ai_act.perform(self.state)
        return external_events

