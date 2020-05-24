import tcod

from input_handlers import handle_main_menu
from graphics.scene.main_menu import MainMenuScene
from globals import GameStates, RenderOrder, CONFIG
from game_map import GameMap
from components.fighter import Fighter
from components.inventory import Inventory
from components.equipment import Equipment
from components.purse import Purse
from components.ai import BasicMonster
from message_log import MessageLog
from entity import Entity

def component(name):
    # TODO: Change this into a proper factory
    component_map = {
        "PLAYER"    : Fighter(hp=70, defense=4, power=5, magic=3),
        "ORC"       : Fighter(hp=10, defense=0, power=3, xp=35),
        "TROLL"     : Fighter(hp=16, defense=1, power=4, xp=100),
        "BASIC"     : BasicMonster(),
        "INVENTORY" : Inventory(26),
        "EQUIPMENT" : Equipment(),
        "PURSE"     : Purse()
    }
    return component_map[name]

def get_game_variables():
    player = Entity(0, 0,
                    '@',
                    tcod.black,
                    'Player',
                    True, 
                    render_order=RenderOrder.ACTOR, 
                    inventory=component("INVENTORY"),
                    equipment=component("EQUIPMENT"),
                    purse=component("PURSE"),
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

    game_state = GameStates.INSTRUCTIONS

    return player, entities, game_map, message_log, game_state


class MainMenuInputHandler:
    def on_key(self, key, state=None):
        return handle_main_menu(key)

class MainMenuState:
    def __init__(self):
        self.error = False
        
    def turn(self, action):
        new_game = action.get('new_game')
        load_saved_game = action.get('load_game')
        exit_game = action.get('exit')
        if self.error and (new_game or load_saved_game or exit_game):
            self.error = False 
            return {}
        elif new_game:
            player, entities, game_map, message_log, game_state = get_game_variables()
            game_state = GameStates.PLAYERS_TURN
            return {
                'next_stage': 'game',
                'args': (player, entities, game_map, message_log, game_state)
            }
        elif load_saved_game:
            try:
                player, entities, game_map, message_log, game_state = load_game()
                return {
                    'next_stage': 'game',
                    'args': (player, entities, game_map, message_log, game_state)
                }
            except:
                self.error = True
        elif exit_game:
            return { 'exit_game': True }
        return {}

class EmptyResultProcess:
    def process(self, event_queue):
        return event_queue

class MainMenuStage:
    def __init__(self):
        self.scene = MainMenuScene()
        self.input_handler = MainMenuInputHandler()
        self.state = MainMenuState()
        self.result_processor = EmptyResultProcess()
        self.event_queue = {}
        self.name = "Main Menu"

    def run(self, events):
        key, mouse_move, mouse_click = events
        self.scene.show(self.state)
        if key:
            action = self.input_handler.on_key(key)
            self.event_queue = self.state.turn(action)
            self.event_queue = self.result_processor.process(self.event_queue)
        return self.event_queue

