import tcod

class CityMenuInputHandler:
    def on_key(self, key, state):
        print("Pressed %s" % key)
        return {}

    def on_mouse_move(self, mouse, state):
        return {}

    def on_mouse_click(self, mouse, state):
        print("Clicked {%s,%s}" % (mouse.x, mouse.y))
        return {}
