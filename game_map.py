import tcod as libtcod
from tile import Tile
from rectangle import Rect
from entity import Entity

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

    def place_entities(self, room, entities, max_monsters, component):
        number_of_monsters = randint(0, max_monsters)
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


    def make_map(self, max_rooms, min_size, max_size, player, entities, max_monsters, components):
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
                self.place_entities(new_room, entities, max_monsters, components)
                rooms.append(new_room)
                num_rooms += 1
    
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles
