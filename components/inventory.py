import tcod as libtcod
from components.tome_factory import make_tome
from message_log import Message

class InventorySlot:
    def __init__(self, item, quantity, capacity=99):
        self.item = item
        self.quantity = quantity
        self.capacity = capacity

    def add(self):
        #TODO: Implement handling of capacity
        pass

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.owner = None
        self.tome_slots = [
            InventorySlot(make_tome("health_tome"), 0),
            InventorySlot(make_tome("magic_missiles"), 0),
            InventorySlot(make_tome("paralysis"), 0),
            InventorySlot(make_tome("fireball"), 0)
        ]

    def add_item(self, item):
        results = []
        results.append({
            'item_added': item,
            'message': Message('You pick up the %s!' % item.name, libtcod.blue)
        })

        tome_slot = list(filter(lambda slot: slot.item.name == item.name, self.tome_slots))
        if len(tome_slot) == 1 and tome_slot[0] is not None:
            tome_slot[0].quantity += 1
        else:
            raise SystemError("Failed to add item to tome slot with name %s" % item.name)
        return results

    def remove_item(self, item):
        self.items.remove(item)

    def remove_item_slot(self, slot):
        self.tome_slots[slot-1].quantity -= 1
        if self.tome_slots[slot-1].quantity < 0:
            raise SystemError("Inventory Slot quantity reduced to below 0")

    def drop(self, item):
        results = []

        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)
        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped %s' % item.name, libtcod.yellow)})

        return results

    def use_hotkey(self, key, **kwargs):
        results = []
        print("Using hotkey %i" % key)
        slot = self.tome_slots[key-1]
        item_component = slot.item.item
        if slot.quantity <= 0:
            results.append({'message': Message('Not enough tomes to cast %s' % slot.item.name, libtcod.yellow) }) 
        elif item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
            results.append({'targeting': slot.item, 'targeting_index': key})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    slot.quantity -= 1
            results.extend(item_use_results)
        return results


    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        tome_slot = list(filter(lambda slot: slot.item.name == item_entity.name, self.tome_slots))
        return self.use_hotkey(self.tome_slots.index(tome_slot)+1)

