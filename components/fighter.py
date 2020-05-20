from message_log import Message
import tcod as libtcod

class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.base_defense = defense
        self.base_power = power
        self.hp = hp
        self.xp = xp
        self.owner = None

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        if self.hp == 0:
            print('%s is dead and yields %i exp' % (self.owner.name, self.xp))
            results.append({'dead': self.owner, 'xp': self.xp})
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
