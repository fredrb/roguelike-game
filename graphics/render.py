import tcod
from globals import CONFIG

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
