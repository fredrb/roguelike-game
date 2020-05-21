import tcod
from message_log import Message

class Chest:
    def __init__(self, money=0):
        self.money = money
        self.owner = None

    def open(self, actor):
        results = []
        results.extend(actor.purse.add_coins(self.money))
        results.append({
            'container_consumed': self.owner
        })
        return results

