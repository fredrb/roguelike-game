from message_log import Message
import random
import tcod as libtcod

class Fighter:
    def __init__(self, hp, defense, power, magic=1, xp=0):
        self.base_max_hp = hp
        self.base_defense = defense
        self.base_power = power
        self.base_magic = magic
        self.hp = hp
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
            if self.owner.purse:
                results.append({'loot': self.owner.purse.coins})
                results.append({'message': 
                    Message('Looted %i gold coins from %s' % (self.owner.purse.coins, self.owner.name), libtcod.light_green)})
            if self.owner.boss:
                results.append({
                    'message': Message('Boss %s slain! Proceed to the stairs' % self.owner.name, libtcod.light_yellow)
                })
                results.append({
                    'boss_dead': True
                })
            results.append({'dead': self.owner})
        return results

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense
        #hit = random.randint(self.power, self.power*10) > random.randint(target.fighter.defense, target.fighter.defense*10)
        damage = random.randint(int(self.power/2), int(self.power*2))
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
