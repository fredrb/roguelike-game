import tcod as libtcod
from message_log import Message

class StrengthUpgrade:
    def __init__(self, factor=1):
        self.factor = factor
        self.stat = "STR"

    def apply(self, fighter):
        fighter.base_power += self.factor
        return {'message': Message('Player got +%i STR' % self.factor, libtcod.light_blue)}

class AgilityUpgrade:
    def __init__(self, factor=1):
        self.factor = factor
        self.stat = "AGI"

    def apply(self, fighter):
        fighter.base_defense += self.factor
        return {'message': Message('Player got +%i AGI' % self.factor, libtcod.light_blue)}

class HPUpgrade:
    def __init__(self, factor=20):
        self.factor = factor
        self.stat = "MAX HP"

    def apply(self, fighter):
        fighter.base_max_hp += self.factor
        return {'message': Message('Player got +%i MAX HP' % self.factor, libtcod.light_blue)}

class Tome:
    def __init__(self, name, price, component):
        self.name = name
        self.price = price
        self.component = component

    @property
    def text(self):
        return "(%i gp): %s [+%i %s]" % (self.price, self.name, self.component.factor, self.component.stat)

    def use(self, actor):
        results = []
        if actor.purse is None:
            return {}
        if actor.fighter is None:
            return {}
        remove_action = actor.purse.remove_coins(self.price)
        results.append(remove_action)
        if remove_action.get('success'):
            results.append(self.component.apply(actor.fighter))
        print("Returning %s" % str(results))
        return results
