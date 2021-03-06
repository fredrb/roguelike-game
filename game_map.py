import tcod as libtcod
from tile import Tile
from rectangle import Rect
from entity import Entity
from components.item import Item
from components.stairs import Stairs
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.shop import Shop
from components.chest import Chest
from components.purse import Purse
from components.monster_factory import make_monster_random, make_monster

from components.factory import make_item

from message_log import Message

from random import randint
from globals import RenderOrder

import math

class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.shopkeeper = None
        self.dungeon_level = dungeon_level

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocked

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_tunnel(self, a1, a2, b, h_dir=True):
        for a in range(min(a1,a2), max(a1,a2) + 1):
            if h_dir:
                self.tiles[a][b].blocked = False
                self.tiles[a][b].block_sight = False
            else:
                self.tiles[b][a].blocked = False
                self.tiles[b][a].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_free(self, entities, x, y):
        if not self.tiles[x][y].blocked:
            for entity in entities:
                if entity.x == x and entity.y == y:
                    return False
            return True
        else:
            return False

    def place_entities(self, room, entities, max_monsters, max_items, component, chest_chance=40):
        max_monsters += math.floor(self.dungeon_level/10)
        number_of_monsters = randint(0, max_monsters)
        number_of_items = randint(0, max_items)

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster = make_monster_random(self.dungeon_level)                    
                monster.x = x
                monster.y = y
                entities.append(monster)

        if randint(0,100) < chest_chance:
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                gold_coins = randint(2*self.dungeon_level,10*self.dungeon_level)
                item_component = Chest(money=gold_coins)
                chest = Entity(x, y, "C", libtcod.darker_orange, 'Chest', True, 
                    render_order=RenderOrder.ITEM,
                    container=item_component) 
                entities.append(chest)

        for i in range(max_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # Item drop roll
                item_chance = randint(0, 100)
                if item_chance < 30: # 30%
                    item = make_item("health_tome")
                elif item_chance < 60: # 30%
                    item = make_item("magic_missiles")
                elif item_chance < 80: # 20%
                    item = make_item("paralysis")
                else: #20%
                    item = make_item("fireball")
                item.x = x
                item.y = y
                entities.append(item)

    def next_floor(self, player, message_log, config, component):
        self.dungeon_level += 1
        entities = [player]
        self.tiles = self.initialize_tiles()
        self.make_map(
            config.get('MAX_ROOMS'), 
            config.get('ROOM_MIN_SIZE'), 
            config.get('ROOM_MAX_SIZE'), 
            player, 
            entities, 
            config.get('MAX_MONSTERS'),
            config.get('MAX_ITEMS'),
            component)

        player.fighter.heal(player.fighter.max_hp // 2)
        message_log.add_message(
            Message('You take a moment to rest', libtcod.light_violet)
        )

        return entities

    def make_boss_map(self, player, entities):
        new_room = Rect(10, 10, 10, 10)
        self.create_room(new_room)

        

        player.x = 12
        player.y = 15

        if (self.dungeon_level <= 7):
            dragon = make_monster('dragon', self.dungeon_level+3, boss=True)
            dragon.x = 18
            dragon.y = 15 
            entities.append(dragon)
        elif (self.dungeon_level <= 14):
            dragon = make_monster('dragon', self.dungeon_level+3, boss=True)
            dragon.x = 18
            dragon.y = 15 
            warlock1 = make_monster('warlock', self.dungeon_level+2)
            warlock1.x = 19
            warlock1.y = 14 
            warlock2 = make_monster('warlock', self.dungeon_level+2)
            warlock2.x = 19
            warlock2.y = 16 
            entities.append(dragon)
            entities.append(warlock1)
            entities.append(warlock2)
        elif (self.dungeon_level <= 28):
            dragon = make_monster('red_dragon', self.dungeon_level+4, boss=True)
            dragon.x = 18
            dragon.y = 15 
            warlock1 = make_monster('warlock', self.dungeon_level+2)
            warlock1.x = 19
            warlock1.y = 11 
            warlock2 = make_monster('warlock', self.dungeon_level+2)
            warlock2.x = 19
            warlock2.y = 19 
            troll1 = make_monster('troll', self.dungeon_level+3)
            troll1.x = 14
            troll1.y = 16
            entities.append(dragon)
            entities.append(warlock1)
            entities.append(warlock2)
        else:
            dragon = make_monster('elder_dragon', self.dungeon_level+4, boss=True)
            dragon.x = 18
            dragon.y = 15 
            troll1 = make_monster('troll_chief', self.dungeon_level+3)
            troll1.x = 14
            troll1.y = 16
            warlock1 = make_monster('shaman', self.dungeon_level+2)
            warlock1.x = 13
            warlock1.y = 11 
            warlock2 = make_monster('shaman', self.dungeon_level+2)
            warlock2.x = 14
            warlock2.y = 19 
            entities.append(dragon)
            entities.append(warlock1)
            entities.append(warlock2)

    def make_light_example(self, player, entities):
        player.x = 12
        player.y = 12
        new_room = Rect(10, 10, 10, 10)
        self.create_room(new_room)
        new_room_2 = Rect(25, 5, 10, 20)
        self.create_room(new_room_2)

        self.create_tunnel(20, 25, 15, True)

        self.tiles[27][12].blocked = True
        self.tiles[27][12].block_sight = True

        self.tiles[29][12].blocked = True
        self.tiles[29][12].block_sight = True

        self.tiles[31][12].blocked = True
        self.tiles[31][12].block_sight = True

        self.tiles[33][12].blocked = True
        self.tiles[33][12].block_sight = True

        self.tiles[27][18].blocked = True
        self.tiles[27][18].block_sight = True

        self.tiles[29][18].blocked = True
        self.tiles[29][18].block_sight = True

        self.tiles[31][18].blocked = True
        self.tiles[31][18].block_sight = True

        self.tiles[33][18].blocked = True
        self.tiles[33][18].block_sight = True




    def make_map(self, max_rooms, min_size, max_size, player, entities, max_monsters, max_items, components):
        if False:
            return self.make_light_example(player, entities)
        if ((self.dungeon_level % 7) == 0):
            return self.make_boss_map(player, entities)
        rooms = []
        num_rooms = 0
        last_room_x = None
        last_room_y = None
        for r in range(max_rooms):
            w = randint(min_size, max_size)
            h = randint(min_size, max_size)
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            new_room = Rect(x, y, w, h)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                last_room_x = new_x
                last_room_y = new_y
                last_corner_x = x+1
                last_corner_y = y+1
                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if randint(0, 1) == 1:
                        self.create_tunnel(prev_x, new_x, prev_y, True)
                        self.create_tunnel(prev_y, new_y, new_x, False)
                    else:
                        self.create_tunnel(prev_y, new_y, prev_x, False)
                        self.create_tunnel(prev_x, new_x, new_y, True)
                self.place_entities(new_room, entities, max_monsters, max_items, components)
                rooms.append(new_room)
                num_rooms += 1


        stairs_component = Stairs(self.dungeon_level+1)
        down_stairs = Entity(last_room_x, last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

        shop_component = Shop(self.dungeon_level)
        self.shopkeeper = Entity(down_stairs.x+1, down_stairs.y+1, '@', libtcod.light_blue, 'Shopkeeper', True,
                            render_order=RenderOrder.ACTOR, shop=shop_component)                    
        entities.append(self.shopkeeper)
        for e in entities:
            if e.x == self.shopkeeper.x and e.y == self.shopkeeper.y and e != self.shopkeeper:
                entities.remove(e)
    
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles
