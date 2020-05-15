from message_log import Message
import tcod as libtcod

class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.owner = None

    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        if self.hp == 0:
            results.append({'dead': self.owner})
        return results

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense
        if damage > 0:
            text = '%s attacks %s for %i hit points' % (self.owner.name.capitalize(), target.name, damage)
            results.append({
                'message': Message(text, libtcod.white)
            })
            results.extend(target.fighter.take_damage(damage))
        else:
            text = '%s attacks %s but does no damage' % (self.owner.name.capitalize(), target.name)
            results.append({
                'message': Message(text, libtcod.white)
            })
        return results
