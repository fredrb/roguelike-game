import tcod 
from menu import main_menu, message_box
from globals import CONFIG

class MainMenuScene:
    def __init__(self):
        self.show_main_menu = True
        self.error = False
        self.main_menu_background_image = tcod.image_load('menu_background.png')
        self.owner = None

    def show(self, state):
        """Show main menu"""
        if self.owner is None:
            raise SystemError("MainMenuStage is detached from render")
        main_menu(self.owner.con,
                  self.main_menu_background_image,
                  CONFIG.get('WIDTH'),
                  CONFIG.get('HEIGHT'))
        if state.error:
            message_box(self.owner.con,
                        'No save game to load',
                        50,
                        CONFIG.get('WIDTH'),
                        CONFIG.get('HEIGHT'))
        tcod.console_flush()
