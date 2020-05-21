from graphics.scene.city import CityMenuScene
from input.city_handler import CityMenuInputHandler
from states import CityMenuState

class CityMenuAct:
    pass

class CityMenuResultProcessor:
    pass

class CityMenuStage:
    def load(self, args):
        pass

    def __init__(self):
        self.scene = CityMenuScene()
        self.input_handler = CityMenuInputHandler()
        self.result_processor = CityMenuResultProcessor()
        self.act = CityMenuAct()
        self.state = CityMenuState()

    def run(self, key):
        print("Running city stage")
        self.scene.show(self.state)
        return {}
