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

class Render:
    def __init__(self):
        tcod.console_set_custom_font(CONFIG.get("FONT_PATH"),
            tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        self.root = None
        self.con = None
        self.panel = None
        self.stages = []

    def __init_screen(self):
        self.root = tcod.console_init_root(
            CONFIG.get('WIDTH'),
            CONFIG.get('HEIGHT'),
            CONFIG.get('TITLE'),
            False,
            None,
            'C',
            True)
        self.con = tcod.console_new(CONFIG.get('WIDTH'), CONFIG.get('HEIGHT'))
        self.panel = tcod.console_new(CONFIG.get('WIDTH'), CONFIG.get('PANEL_HEIGHT'))

    def clear(self):
        self.con.clear()

    def start(self, stages):
        for stage in stages:
            stage.owner = self
            self.stages.append(stage)
        self.__init_screen()
