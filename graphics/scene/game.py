from globals import CONFIG, GameStates
from menu import render_bar, inventory_menu, character_screen, level_up_menu, menu, shop_menu, stats_key_value, help_menu
import tcod
import math

class GameScene:
    def __init__(self):
        self.fov_recompute = True
        self.redraw = True

        self.owner = None
        # TODO: Move fov_map to game_map
        self.fov_map = None

    def show(self, state):
        self.error = state.error
        if self.owner is None:
            raise SystemError("MainMenuStage is detached from render")
        self.__make_map_if_none(state)
        self.__fov_recompute(state)
        self.__render_all(state)
        self.redraw = True
        self.fov_recompute = False
        tcod.console_flush()
        self.__clear_all(state)

    def __make_map_if_none(self, state):
        if self.fov_map is None:
            self.fov_map = GameScene.init_fov_map(state.game_map)

    def __clear_all(self, state):
        #TODO: Clear the whole screen? Maybe this is why we have menu text lingering
        for entity in state.entities:
            tcod.console_put_char(self.owner.con, entity.x, entity.y, ' ', tcod.BKGND_NONE)

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def __show_stats(self, con, state):
        self.__clear_all(state)
        tcod.console_clear(con)
        history = state.history
        con.draw_frame(0, 0, CONFIG.get('MAP_WIDTH'), CONFIG.get('MAP_HEIGHT'), "STATS", True, tcod.white, tcod.darker_grey)
        stats_key_value(con, "Killed by", "(%s) %s" % (history.killed_by.char, history.killed_by.name),
                        0, history.killed_by.color, CONFIG.get('MAP_WIDTH'))

        stats_key_value(con, "Dungeon Level", str(state.game_map.dungeon_level), 2, tcod.light_yellow, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Turns Survived", str(history.turns), 4, tcod.light_yellow, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Damage Dealt", str(history.damage_dealt), 7, tcod.red, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Magic Damage Dealt", str(history.magic_damage), 9, tcod.red, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Damage Received", str(history.damage_received), 11, tcod.red, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Healing Done", str(history.healed), 13, tcod.green, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Creatures Paralyzed", str(history.paralyzed), 15, tcod.purple, CONFIG.get('MAP_WIDTH'))
        most_killed = history.most_killed_enemy()
        stats_key_value(con, "Most Killed Enemy", "(%i) %s" % (most_killed[1], most_killed[0]), 18, tcod.red, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Chest Open", str(history.chests_open), 21, tcod.light_yellow, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Items Picked-up", str(history.items_picked), 24, tcod.light_yellow, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Bosses Defeated", str(history.bosses_killed), 27, tcod.light_yellow, CONFIG.get('MAP_WIDTH'))
        stats_key_value(con, "Elder Dragons Defeated", str(history.elder_dragons_killed), 29, tcod.cyan, CONFIG.get('MAP_WIDTH'))

        tcod.console_set_default_foreground(con, tcod.white)
        con.vline(int(CONFIG.get('MAP_WIDTH')/2)-1, 2, 40)
        tcod.console_blit(self.owner.con, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('MAP_HEIGHT'), 0, 0, CONFIG.get('MAP_Y'))

    def __render_all(self, state):
        con = self.owner.con
        panel = self.owner.panel
        hotkeys = self.owner.hotkeys
        upper_bar = self.owner.upper_bar
        colors = CONFIG.get('COLORS')

        if state.game_state == GameStates.PLAYER_DEAD:
            self.__show_stats(con, state)
            tcod.console_set_default_foreground(upper_bar, tcod.white)
            tcod.console_set_default_background(upper_bar, tcod.black)
            tcod.console_clear(upper_bar)
            tcod.console_blit(self.owner.upper_bar, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('UPPER_BAR_HEIGHT'), 0, 0, 0)
        else:
            offset_mouse_x = state.mouse_x
            offset_mouse_y = state.mouse_y - CONFIG.get('MAP_Y')
            if self.fov_recompute or state.game_state == GameStates.TARGETING or self.redraw:
                for y in range(state.game_map.height):
                    for x in range(state.game_map.width):
                        visible = tcod.map_is_in_fov(self.fov_map, x, y)
                        wall = state.game_map.tiles[x][y].block_sight
                        if  visible:
                            if wall:
                                tcod.console_set_char_background(con, x, y, colors.get('light_wall'), tcod.BKGND_SET)
                            else:
                                tcod.console_set_char_background(con, x, y, colors.get('light_ground'), tcod.BKGND_SET)
                                if state.game_state == GameStates.TARGETING:
                                    if state.targeting_area and self.distance(x, y, offset_mouse_x, offset_mouse_y) <= state.targeting_radius:
                                        tcod.console_set_char_background(con, x, y, tcod.light_red, tcod.BKGND_SET)
                                    elif x == offset_mouse_x and y == offset_mouse_y:
                                        tcod.console_set_char_background(con, x, y, tcod.light_red, tcod.BKGND_SET)
                                        
                                if state.game_state == GameStates.TARGETING and x == offset_mouse_x and y == offset_mouse_y:
                                    if state.targeting_area:
                                        radius = state.targeting_radius
                                    tcod.console_set_char_background(con, x, y, tcod.light_red, tcod.BKGND_SET)
                            state.game_map.tiles[x][y].explored = True
                            if self.redraw and state.game_state in (GameStates.PLAYERS_TURN, GameStates.TARGETING):
                                tcod.console_put_char(con, x, y, ' ', tcod.BKGND_NONE)
                        elif state.game_map.tiles[x][y].explored:
                            if wall:
                                tcod.console_set_char_background(con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
                            else:
                                tcod.console_set_char_background(con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)
                            if self.redraw and state.game_state in (GameStates.PLAYERS_TURN, GameStates.TARGETING):
                                tcod.console_put_char(con, x, y, ' ', tcod.BKGND_NONE)
                        elif self.redraw and state.game_state in (GameStates.PLAYERS_TURN, GameStates.TARGETING):
                            tcod.console_put_char(con, x, y, ' ', tcod.BKGND_NONE)

            tcod.console_set_default_background(hotkeys, tcod.black)
            tcod.console_clear(hotkeys)
            tcod.console_set_default_background(panel, tcod.black)
            tcod.console_clear(panel)
            for e in sorted(state.entities, key=lambda x: x.render_order.value):
                #if tcod.map_is_in_fov(self.self.fov_map, e.x, e.y) or (e.stairs and self.game_map.tiles[e.x][e.y].explored):
                if tcod.map_is_in_fov(self.fov_map, e.x, e.y) or (e.stairs):
                    tcod.console_set_default_foreground(con, e.color)
                    tcod.console_put_char(con, e.x, e.y, e.char, tcod.BKGND_NONE)


            # Monster scan
            monster_scan = 1
            max_monster_scan = 4
            item_scan = 1
            max_item_scan = 6
            tcod.console_set_default_foreground(hotkeys, tcod.light_grey)
            hotkeys.print_(22, monster_scan, "Monster Scan", tcod.BKGND_NONE)

            tcod.console_set_default_foreground(panel, tcod.light_grey)
            tcod.console_print_ex(panel, 1, 1, tcod.BKGND_NONE, tcod.LEFT, "Ground Scan")

            for e in reversed(sorted(state.entities, key=lambda x: x.render_order.value)):
                if tcod.map_is_in_fov(self.fov_map, e.x, e.y) or (e.stairs):
                    if monster_scan < max_monster_scan and e.ai is not None and e.fighter is not None:
                        monster_scan += 1 
                        hotkeys.print_box(22, monster_scan, 20, 1, e.name, tcod.white, tcod.black, tcod.BKGND_NONE, tcod.RIGHT)
                        tcod.console_set_default_foreground(hotkeys, e.color)
                        tcod.console_put_char(hotkeys, 43, monster_scan, e.char, tcod.BKGND_NONE)
                        render_bar(hotkeys, 45, monster_scan, 30, 'HP', e.fighter.hp, e.fighter.max_hp, tcod.light_red, tcod.darker_red)

                    if item_scan < max_item_scan and e.ai is None and e != state.player:
                        item_scan += 1
                        tcod.console_set_default_foreground(panel, e.color)
                        tcod.console_put_char(panel, 1, item_scan, e.char, tcod.BKGND_NONE)
                        tcod.console_set_default_foreground(panel, tcod.white)
                        tcod.console_print_ex(panel, 3, item_scan, tcod.BKGND_NONE, tcod.LEFT, e.name[:19])
            #tcod.console_set_char_background(panel, 10, 10, tcod.violet, tcod.BKGND_SET)

            # Message Log
            y = 1
            for message in state.message_log.messages:
                tcod.console_set_default_foreground(panel, message.color)
                tcod.console_print_ex(panel, state.message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
                y += 1

            # Hotkeys
            slot_pos = 0
            for slot in state.player.inventory.tome_slots:
                rel_pos = (slot_pos*3)
                hotkeys.draw_frame(rel_pos+1, 1, 3, 3, str(slot_pos+1), True, tcod.white, tcod.grey) 
                if slot.quantity > 0:
                    tcod.console_set_default_foreground(hotkeys, slot.item.color)
                else:
                    tcod.console_set_default_foreground(hotkeys, tcod.light_grey)
                tcod.console_print_ex(hotkeys,rel_pos+2, 2, tcod.BKGND_NONE, tcod.LEFT, "#")
                tcod.console_set_default_foreground(hotkeys, tcod.white)
                tcod.console_print_ex(hotkeys,rel_pos+1, 4, tcod.BKGND_NONE, tcod.LEFT, "x%i" % slot.quantity)
                slot_pos += 1


            # Upper bar (health and stats)
            tcod.console_set_default_foreground(upper_bar, tcod.white)
            tcod.console_set_default_background(upper_bar, tcod.black)
            tcod.console_clear(upper_bar)
            tcod.console_print_ex(upper_bar, 1, 1, tcod.BKGND_NONE, tcod.LEFT, 'Player')
            tcod.console_set_default_foreground(upper_bar, tcod.black)
            tcod.console_set_default_background(upper_bar, tcod.white)
            tcod.console_print_ex(upper_bar, 7, 1, tcod.BKGND_SET, tcod.LEFT, '@')
            tcod.console_set_default_foreground(upper_bar, tcod.white)
            tcod.console_set_default_background(upper_bar, tcod.black)


            render_bar(upper_bar, 12, 1, CONFIG.get('BAR_WIDTH'), 'HP', state.player.fighter.hp, state.player.fighter.max_hp,
                       tcod.light_red, tcod.darker_red)

            upper_bar.print_box(35, 1, 14, 1, 'Dungeon Level:', tcod.light_grey, tcod.black, tcod.BKGND_NONE, tcod.RIGHT)
            upper_bar.print_box(35, 2, 14, 1, 'Gold Coins:', tcod.light_grey, tcod.black, tcod.BKGND_NONE, tcod.RIGHT)
            tcod.console_set_default_foreground(upper_bar, tcod.light_yellow)
            tcod.console_print_ex(upper_bar, 49, 1, tcod.BKGND_NONE, tcod.LEFT, '%i' % state.game_map.dungeon_level)
            tcod.console_print_ex(upper_bar, 49, 2, tcod.BKGND_NONE, tcod.LEFT, '%i' % state.player.purse.coins)

            upper_bar.print_box(60, 1, 9, 1, 'Power:', tcod.light_grey, tcod.black, tcod.BKGND_NONE, tcod.RIGHT)
            upper_bar.print_box(60, 2, 9, 1, 'Defense:', tcod.light_grey, tcod.black, tcod.BKGND_NONE, tcod.RIGHT)
            upper_bar.print_box(60, 3, 9, 1, 'Maigc:', tcod.light_grey, tcod.black, tcod.BKGND_NONE, tcod.RIGHT)
            tcod.console_set_default_foreground(upper_bar, tcod.white)
            tcod.console_print_ex(upper_bar, 69, 1, tcod.BKGND_NONE, tcod.LEFT, '%i' % state.player.fighter.base_power)
            tcod.console_print_ex(upper_bar, 69, 2, tcod.BKGND_NONE, tcod.LEFT, '%i' % state.player.fighter.base_defense)
            tcod.console_print_ex(upper_bar, 69, 3, tcod.BKGND_NONE, tcod.LEFT, '%i' % state.player.fighter.base_magic)

            # Print all consoles
            tcod.console_blit(self.owner.upper_bar, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('UPPER_BAR_HEIGHT'), 0, 0, 0)
            tcod.console_blit(self.owner.con, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('MAP_HEIGHT'), 0, 0, CONFIG.get('MAP_Y'))
            tcod.console_blit(self.owner.panel, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('PANEL_HEIGHT'), 0, 0, CONFIG.get('PANEL_Y'))
            tcod.console_blit(self.owner.hotkeys, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('ACTION_HEIGHT'), 0, 0, CONFIG.get('ACTION_Y'))

            # Overlay menus
            if state.game_state == GameStates.INSTRUCTIONS:
                help_menu(con, CONFIG.get('WIDTH'))

            if state.game_state == GameStates.SHOP:
                shop_menu(con, state.player, state.game_map.shopkeeper.shop, CONFIG.get('WIDTH'), CONFIG.get('HEIGHT'))

            if state.game_state in (GameStates.INVENTORY, GameStates.DROP_INVENTORY):
                if state.game_state == GameStates.INVENTORY:
                    title = 'Press the key next to an item to use it or I again to leave\n'
                else:
                    title = 'Press the key next to an item to drop it or O again to leave\n'
                inventory_menu(con, title, state.player, 50, CONFIG.get('WIDTH'), CONFIG.get('HEIGHT'))

            if state.game_state == GameStates.CHARACTER_SCREEN:
                character_screen(state.player, 30, 10, CONFIG.get("WIDTH"), CONFIG.get("HEIGHT"))

            if state.game_state == GameStates.LEVEL_UP:
                level_up_menu(self.owner.con, 'Level Up! Choose a stat to raise:', state.player, 40, CONFIG.get('WIDTH'), CONFIG.get('HEIGHT'))


    def __fov_recompute(self, state):
        if self.fov_recompute:
            self.__recompute_fov(state.player.x, state.player.y)

    def __recompute_fov(self, player_x, player_y):
        self.fov_map.compute_fov(
            player_x,
            player_y,
            CONFIG.get('FOV_RADIUS'),
            CONFIG.get('FOV_LIGHT_WALLS'),
            CONFIG.get('FOV_ALGORITHM'))

    @staticmethod
    def init_fov_map(game_map):
        """Initializes a new instance of tcod.Map based on local self.game_map instance"""
        fov_map = tcod.map.Map(game_map.width, game_map.height)
        for y in range(game_map.height):
            for x in range(game_map.width):
                fov_map.transparent[y, x] = not game_map.tiles[x][y].block_sight
                fov_map.walkable[y, x] = not game_map.tiles[x][y].blocked
        return fov_map
