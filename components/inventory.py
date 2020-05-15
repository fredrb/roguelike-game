import tcod as libtcod
from message_log import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []
        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full',
                                   libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the %s!' % item.name, libtcod.blue)
            })
            self.items.append(item)
        return results
