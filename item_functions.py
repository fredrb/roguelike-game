import tcod as libtcod
import random
import math
from message_log import Message
from components.ai import ConfusedMonster, ParalysedMonster
from functools import reduce

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    base_heal = math.ceil(entity.fighter.base_magic/4)*5 + amount + math.ceil(entity.fighter.base_max_hp*0.1)
    if entity.fighter.hp == entity.fighter.base_max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full HP', libtcod.yellow)})
    else:
        rolled_amount = random.randint(math.ceil(base_heal/1.5), base_heal*2)
        entity.fighter.heal(rolled_amount)
        results.append({
            'consumed': True,
            'message': Message('Tome of Healing recovered %i HP' % rolled_amount, libtcod.green),
            'stat_heal': rolled_amount
        })

    return results

def cast_magic_missile(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    damage = kwargs.get('damage')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({
            'consumed': False,
            'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)
        })
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            factor = caster.fighter.base_magic
            print("Factor: %i" % factor)
            #missiles = math.ceil(factor/10)
            missiles = math.ceil(math.log(factor, 10) + math.ceil(factor/100))
            base_dmg = math.ceil((damage + factor)/2)
            print("missiles %i" % missiles)
            dmg = [random.randint(int(base_dmg/4), int(base_dmg*1.5)) for _ in range(missiles)]
            print("%s" % str(dmg))
            rolled_dmg = reduce(lambda x,acc: acc+x, dmg)
            print("final damage: %s" % str(rolled_dmg))
            results.extend(entity.fighter.take_damage(rolled_dmg))
            results.append({
                'consumed': True,
                'message': Message('%i magic missile(s) hit %s. Damage taken: %i' % (missiles, entity.name, rolled_dmg), libtcod.cyan),
                'stat_magic_damage': rolled_dmg
            })
            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results

def cast_fireball(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), libtcod.orange)})

    base_dmg = math.ceil(caster.fighter.base_magic * (damage*0.1)) + damage
    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            rolled_dmg = random.randint(int(base_dmg/2), base_dmg*2)
            results.append({
                'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, rolled_dmg), libtcod.orange),
                'stat_magic_damage': rolled_dmg
            })
            results.extend(entity.fighter.take_damage(rolled_dmg))
    return results

def cast_paralysis(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({
            'consumed': False,
            'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)
        })
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            turns = 10 + math.ceil(caster.fighter.base_magic/10) 
            confused_ai = ParalysedMonster(entity.ai, turns)
            confused_ai.owner = entity
            entity.ai = confused_ai
            results.append({
                'consumed': True,
                'message': Message('%s is paralysed for %i turns' % (entity.name, turns), libtcod.light_cyan),
                'stat_paralyzed': True
            })
            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results
def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} look vacant, as he starts to stumble around!'.format(entity.name), libtcod.light_green)})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results
