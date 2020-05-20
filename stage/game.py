from graphics.scene.game import GameScene
from globals import GameStates
from input_handlers import handle_keys

class GameInputHandler:
    def on_key(self, key, state):
        return handle_keys(key, state.game_state)

class GameState():
    def __init__(self):
        self.error = None
        self.entities = []
        # TODO: change
        self.game_state = GameStates.PLAYERS_TURN
        self.previous_game_state = None
        self.message_log = None
        self.player = None
        self.targeting_item = None

class GameAct():
    pass

class GameStateReporter():
    pass

class GameStage:
    def __init__(self):
        self.scene = GameScene()
        self.input_handler = handle_keys
        self.act = GameAct()
        self.state = GameState()
        self.reporter = GameStateReporter()
