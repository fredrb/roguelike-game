import math
import tcod as libtcod

from globals import RenderOrder
from components.item import Item

class Entity:
    """
    Generic representation of players, enemies and any interactable object
    """
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, 
        fighter=None, 
        ai=None,
        item=None,
        stairs=None,
        level=None,
        equipment=None,
        equippable=None,
        shop=None,
        purse=None,
        container=None,
        inventory=None):

        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.render_order = render_order
        self.stairs = stairs
        self.equipment = equipment
        self.equippable = equippable
        self.level = level
        self.shop = shop
        self.purse = purse
        self.container = container

        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self
        if self.item:
            self.item.owner = self
        if self.inventory:
            self.inventory.owner = self
        if self.stairs:
            self.stairs.owner = self
        if self.level:
            self.level.owner = self
        if self.equipment:
            self.equipment.owner = self
        if self.purse:
            self.purse.owner = self
        if self.shop:
            self.shop.owner = self
        if self.container:
            self.container.owner = self
        if self.equippable:
            self.equippable.owner = self
            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_towards(self, tx, ty, game_map, entities):
        dx = tx - self.x
        dy = ty - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx/distance))
        dy = int(round(dy/distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or Entity.get_blocking(entities, dx, dy)):
            self.move(dx, dy)

    def distance_to(self, other):
       dx = other.x - self.x
       dy = other.y - self.y
       return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_astar(self, target, entities, game_map):
        fov = libtcod.map_new(game_map.width, game_map.height)
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        my_path = libtcod.path_new_using_map(fov, 1.41)

        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, game_map, entities)
        libtcod.path_delete(my_path)

    @staticmethod
    def get_blocking(entities, dest_x, dest_y):
        for e in entities:
            if e.blocks and e.x == dest_x and e.y == dest_y:
                return e
        return None
