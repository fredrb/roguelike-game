import tcod
from menu import city_bg
from globals import CONFIG

class CityMenuScene:
    def __init__(self):
        self.main_menu_background_image = tcod.image_load('bg_metano.png')
        self.owner = None

    def show(self, state):
        """Show city shop menu"""
        print("Showing city menu")
        if self.owner is None:
            raise SystemError("CityMenuScene is detached from render")
        city_bg(self.owner.root,
            self.main_menu_background_image,
            CONFIG.get('WIDTH'),
            CONFIG.get('HEIGHT'))
        tcod.console_flush()
