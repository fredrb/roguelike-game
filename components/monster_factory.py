from components.fighter import Fighter
from components.purse import Purse
from components.ai import BasicMonster, SummonerMonster
from entity import Entity
from globals import RenderOrder
import tcod
import random 

class MonsterFactory:
    def base_monster(self, base_hp=1, hp_factor=0, base_def=0, def_factor=0, base_power=0, power_factor=0):
        self.base_hp = base_hp
        self.hp_factor = hp_factor
        self.base_def = base_def
        self.def_factor = def_factor
        self.base_power = base_power
        self.power_factor = power_factor

    def __get_hp(self, level):
        return self.base_hp + (level*self.hp_factor)
    
    def __get_defense(self, level):
        return self.base_def + (level*self.def_factor)

    def __get_power(self, level):
        return self.base_power + (level*self.power_factor)

    def get_fighter(self, level):
        return Fighter(
            hp=self.__get_hp(level),
            defense=self.__get_defense(level),
            power=self.__get_power(level))


class GoblinFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(6, 3, 0, 1, 0, 1)
    
    def make(self, level, boss):
        monster = Entity(0, 0, 'g', tcod.desaturated_green, 'Goblin', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(1*level,5*level)),
                         level=level, ai=BasicMonster()) 
        return monster

class GoblinWarriorFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(10, 3, 0, 2, 1, 2)
    
    def make(self, level, boss):
        monster = Entity(0, 0, 'g', tcod.dark_green, 'Goblin Warrior', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(2*level,6*level)),
                         level=level,
                         ai=BasicMonster())
        return monster

class GoblinWarlockFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(20, 4, 1, 2, 1, 2)

    def make(self, level, boss):
        monster = Entity(0, 0, 'w', tcod.purple, 'Goblin Warlock', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(6*level,9*level)),
                         level=level,
                         ai=SummonerMonster(summon='goblin', chance=20))
        return monster

class GoblinChiefFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(20, 3, 2, 2, 3, 2)
    
    def make(self, level, boss):
        monster = Entity(0, 0, 'G', tcod.dark_green, 'Goblin Chief', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(4*level,7*level)),
                         level=level,
                         ai=BasicMonster())
        return monster

class TrollFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(40, 4, 3, 3, 5, 2)
    
    def make(self, level, boss):
        monster = Entity(0, 0, 'T', tcod.light_red, 'Troll', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(4*level,8*level)),
                         level=level,
                         ai=BasicMonster())
        return monster

class TrollShamanFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(50, 6, 2, 1, 5, 1)
    
    def make(self, level, boss):
        monster = Entity(0, 0, 'S', tcod.light_red, 'Troll Shaman', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(4*level,8*level)),
                         level=level,
                         ai=SummonerMonster(summon='troll', chance=25))
        return monster

class TrollChiefFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(60, 6, 5, 10, 12, 10)
    
    def make(self, level, boss):
        monster = Entity(0, 0, 'T', tcod.dark_red, 'Troll Chief', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(6*level,9*level)),
                         level=level,
                         ai=BasicMonster())
        return monster

class DragonFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(800, 50, 90, 12, 30, 14)
    
    def make(self, level, boss):
        monster = Entity(0, 0, 'D', tcod.dark_green, 'Green Dragon', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(12*level,24*level)),
                         level=level,
                         boss=boss,
                         ai=BasicMonster())
        return monster

class RedDragonFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(3650, 100, 18, 16, 52, 18)
    
    def make(self, level, boss):
        monster = Entity(0, 0, 'D', tcod.red, 'Red Dragon', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(18*level,35*level)),
                         level=level,
                         boss=boss,
                         ai=BasicMonster())
        return monster

class ElderDragonFactory(MonsterFactory):
    def __init__(self):
        super().base_monster(13650, 200, 48, 19, 92, 32)
    
    def make(self, level, boss):
        monster = Entity(0, 0, 'D', tcod.cyan, 'Elder Dragon', True,
                         render_order=RenderOrder.ACTOR,
                         fighter=super().get_fighter(level),
                         purse=Purse(initial=random.randint(98*level,135*level)),
                         level=level,
                         boss=boss,
                         ai=BasicMonster())
        return monster


def make_monster(name, level, boss=False):
    factory_map = {
        'goblin': GoblinFactory(),
        'troll': TrollFactory(),
        'warlock': GoblinWarlockFactory(),
        'shaman': TrollShamanFactory(),
        'dragon': DragonFactory(),
        'red_dragon': RedDragonFactory(),
        'elder_dragon': ElderDragonFactory()
    }
    return factory_map[name].make(level, boss)

def make_monster_random(level):
    if level == 1:
        return random.choice([GoblinFactory(), GoblinWarriorFactory()]).make(level, False) 
    elif level < 3:
        return random.choice([GoblinFactory(), GoblinWarriorFactory(), GoblinWarlockFactory()]).make(level, False) 
    elif level < 6:
        return random.choice([GoblinFactory(), GoblinWarriorFactory(), GoblinWarlockFactory(), GoblinChiefFactory()]).make(level, False) 
    elif level < 8:
        return random.choice([GoblinWarriorFactory(), GoblinWarlockFactory(), GoblinChiefFactory(), TrollFactory()]).make(level, False) 
    elif level < 12:
        return random.choice([GoblinWarlockFactory(), GoblinChiefFactory(), TrollFactory(), TrollShamanFactory()]).make(level, False) 
    elif level < 18:
        return random.choice([GoblinWarlockFactory(), TrollFactory(), TrollChiefFactory(), TrollShamanFactory(), DragonFactory()]).make(level, False) 
    elif level < 22:
        return random.choice([TrollFactory(), TrollChiefFactory(), DragonFactory(), RedDragonFactory()]).make(level, False) 
    else:
        return random.choice([DragonFactory(), RedDragonFactory()]).make(level, False) 

