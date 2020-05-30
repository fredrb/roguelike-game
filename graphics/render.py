import tcod
import sys
import os

from globals import CONFIG


class Render:

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    def __init__(self):
        res = Render.resource_path(CONFIG.get("FONT_PATH"))
        tcod.console_set_custom_font(res,
            tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        self.root = None
        self.con = None
        self.panel = None
        self.hotkeys = None
        self.upper_bar = None
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
        self.hotkeys = tcod.console_new(CONFIG.get('WIDTH'), CONFIG.get('ACTION_HEIGHT'))
        self.panel = tcod.console_new(CONFIG.get('WIDTH'), CONFIG.get('PANEL_HEIGHT'))
        self.upper_bar = tcod.console_new(CONFIG.get('WIDTH'), CONFIG.get('UPPER_BAR_HEIGHT'))

    def clear(self):
        self.con.clear()

    def start(self, stages):
        for stage in stages:
            stage.owner = self
            self.stages.append(stage)
        self.__init_screen()
