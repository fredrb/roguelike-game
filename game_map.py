import tcod as libtcod
from tile import Tile
from rectangle import Rect
from entity import Entity
from components.item import Item
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse

from message_log import Message

from random import randint
from globals import RenderOrder

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

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

    def place_entities(self, room, entities, max_monsters, max_items, component):
        number_of_monsters = randint(0, max_monsters)
        number_of_items = randint(0, max_items)

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', True,
                                     render_order=RenderOrder.ACTOR,
                                     fighter=component("ORC"),
                                     ai=component("BASIC"))
                else:
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', True,
                                     render_order=RenderOrder.ACTOR,
                                     fighter=component("TROLL"),
                                     ai=component("BASIC"))
                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # Item drop roll
                item_chance = randint(0, 100)
                if item_chance < 30:
                    item_component = Item(use_function=heal, amount=4)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', 
                        render_order=RenderOrder.ITEM,
                        item=item_component)
                elif item_chance < 80:
                    msg=Message('Click on an enemy to confuse it, or right-click to cancel', libtcod.light_cyan)
                    item_component = Item(use_function=cast_confuse,
                        targeting=True,
                        targeting_message=msg)
                    item = Entity(x, y, '#', libtcod.light_pink, 'Confusion Scroll',
                        render_order=RenderOrder.ITEM,
                        item=item_component)

                elif item_chance < 90:
                    msg=Message('Left-click to cast, right-click to cancel', libtcod.light_cyan)
                    item_component = Item(use_function=cast_fireball, 
                        targeting=True,
                        targeting_message=msg,
                        damage=60, 
                        radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll',
                        render_order=RenderOrder.ITEM,
                        item=item_component)
                else:
                    item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll',
                        render_order=RenderOrder.ITEM,
                        item=item_component)
                entities.append(item)


    def make_map(self, max_rooms, min_size, max_size, player, entities, max_monsters, max_items, components):
        rooms = []
        num_rooms = 0
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
    
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles