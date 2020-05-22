from message_log import Message
import tcod as libtcod

class Purse:
    def __init__(self, initial=0, max_coins=9999):
        self.coins = initial
        self.max_coins = max_coins

    def remove_coins(self, amount):
        if amount > self.coins:
            return {'success': False, 'message': Message("Not enough gold to buy item", libtcod.light_yellow)}
        self.coins -= amount
        return {'success': True}

    def add_coins(self, amount):
        results = []
        new_amount = self.coins + amount
        if new_amount > self.max_coins:
            results.append({
                'message': Message('Maximum money (%i) reached' % self.max_coins, libtcod.yellow) 
            })
            self.coins = self.max_coins
        else:
            self.coins = new_amount
            results.append({
                'message': Message('Added %i gold coins to purse' % amount, libtcod.green)
            })
        return results
        

