from globals import CONFIG, GameStates
from menu import render_bar, inventory_menu, character_screen, level_up_menu, menu
import tcod

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

    def __render_all(self, state):
        con = self.owner.con
        panel = self.owner.panel
        colors = CONFIG.get('COLORS')
        if self.fov_recompute:
            for y in range(state.game_map.height):
                for x in range(state.game_map.width):
                    visible = tcod.map_is_in_fov(self.fov_map, x, y)
                    wall = state.game_map.tiles[x][y].block_sight
                    if  visible:
                        if wall:
                            tcod.console_set_char_background(con, x, y, colors.get('light_wall'), tcod.BKGND_SET)
                        else:
                            tcod.console_set_char_background(con, x, y, colors.get('light_ground'), tcod.BKGND_SET)
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

        for e in sorted(state.entities, key=lambda x: x.render_order.value):
            #if tcod.map_is_in_fov(self.self.fov_map, e.x, e.y) or (e.stairs and self.game_map.tiles[e.x][e.y].explored):
            if tcod.map_is_in_fov(self.fov_map, e.x, e.y) or (e.stairs):
                tcod.console_set_default_foreground(con, e.color)
                tcod.console_put_char(con, e.x, e.y, e.char, tcod.BKGND_NONE)

        tcod.console_set_char_background(panel, 10, 10, tcod.violet, tcod.BKGND_SET)

        tcod.console_set_default_background(panel, tcod.black)
        tcod.console_clear(panel)
        y = 1
        for message in state.message_log.messages:
            tcod.console_set_default_foreground(panel, message.color)
            tcod.console_print_ex(panel, state.message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
            y += 1

        render_bar(panel, 1, 1, CONFIG.get('BAR_WIDTH'), 'HP', state.player.fighter.hp, state.player.fighter.max_hp,
                   tcod.light_red, tcod.darker_red)
        tcod.console_print_ex(panel, 1, 3, tcod.BKGND_NONE, tcod.LEFT, 
                                 'Dungeon Level: %s' % state.game_map.dungeon_level)

        tcod.console_print_ex(panel, 1, 4, tcod.BKGND_NONE, tcod.LEFT,
                                 'Gold Coins: %i' % state.player.purse.coins)

        tcod.console_blit(self.owner.con, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('HEIGHT'), 0, 0, 0)
        tcod.console_blit(self.owner.panel, 0, 0, CONFIG.get('WIDTH'), CONFIG.get('PANEL_HEIGHT'), 0, 0, CONFIG.get('PANEL_Y'))

        if state.game_state == GameStates.SHOP:
            title = 'Shop at level %s' % state.game_map.dungeon_level
            menu(con, title, ['(1) +1 STR (Stronger attacks)'], 50, CONFIG.get('WIDTH'), CONFIG.get('HEIGHT'))

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
