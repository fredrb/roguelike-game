from components.fighter import Fighter
from components.ai import BasicMonster
from components.inventory import Inventory
from components.equipment import Equipment
from components.item import Item
from item_functions import heal, cast_magic_missile, cast_paralysis, cast_fireball
from entity import Entity
from message_log import Message
from globals import RenderOrder

import tcod

class HealthTomeFactory:
    def make(self):
        item_component = Item(use_function=heal, amount=4)
        item = Entity(0, 0, '#', tcod.violet, 'Healing Tome', True,
            render_order=RenderOrder.ITEM,
            item=item_component)
        return item

class MagicMissileFactory:
    def make(self):
        target_msg = Message('Left-click to cast, right-click to cancel', tcod.light_cyan)
        item_component = Item(use_function=cast_magic_missile,
            targeting=True,
            targeting_message=target_msg,
            damage=12)
        item = Entity(0, 0, '#', tcod.blue, 'Magic Missile Tome', True,
            render_order=RenderOrder.ITEM,
            item=item_component)
        return item

class ParalysisTomeFactory:
    def make(self):
        target_msg = Message('Left-click to cast, right-click to cancel', tcod.light_cyan)
        item_component = Item(use_function=cast_paralysis,
            targeting=True,
            targeting_message=target_msg)
        item = Entity(0, 0, '#', tcod.pink, 'Paralysis Tome', True,
            render_order=RenderOrder.ITEM,
            item=item_component)
        return item

class FireBallTomeFactory:
    def make(self):
        target_msg = Message('Left-click to cast, right-click to cancel', tcod.light_cyan)
        item_component = Item(use_function=cast_fireball,
            radius=1,
            damage=10,
            targeting=True,
            targeting_area=True,
            targeting_message=target_msg)
        item = Entity(0, 0, '#', tcod.red, 'Fireball Tome', True,
            render_order=RenderOrder.ITEM,
            item=item_component)
        return item

def component(name):
    # TODO: Change this into a proper factory
    component_map = {
        "PLAYER"    : Fighter(hp=60, defense=2, power=5),
        "ORC"       : Fighter(hp=10, defense=0, power=3, xp=35),
        "TROLL"     : Fighter(hp=16, defense=1, power=4, xp=100),
        "BASIC"     : BasicMonster(),
        "INVENTORY" : Inventory(26),
        "EQUIPMENT" : Equipment()
    }
    return component_map[name]


def make_item(name):
    factory_map = {
        "health_tome": HealthTomeFactory(),
        "magic_missiles": MagicMissileFactory(),
        "paralysis": ParalysisTomeFactory(),
        "fireball": FireBallTomeFactory()
    }
    return factory_map[name].make()
