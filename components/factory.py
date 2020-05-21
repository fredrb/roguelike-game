from components.fighter import Fighter
from components.ai import BasicMonster
from components.inventory import Inventory
from components.equipment import Equipment

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

