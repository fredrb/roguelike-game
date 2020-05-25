import tcod as libtcod

def render_option(option_text, index, window, y):
    text = '(' + str(index) + ') ' + option_text
    libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)

def render_shopoption(option, index, window, y):
    x = 0
    text = '(' + str(index) + '):'
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
    x += len(str(index))+3
    price = '%i gp' % option.price
    libtcod.console_set_default_foreground(window, libtcod.light_yellow)
    libtcod.console_print_ex(window, x, y, libtcod.BKGND_NONE, libtcod.LEFT, price)
    x += len(price)+1

    libtcod.console_set_default_foreground(window, libtcod.cyan)
    libtcod.console_print_ex(window, x, y, libtcod.BKGND_NONE, libtcod.LEFT, option.bonus)
    x += len(option.bonus)+1

    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_ex(window, x, y, libtcod.BKGND_NONE, libtcod.LEFT, option.name)


def menu(con, header, options, width, screen_width, screen_height,
         render_func=render_option):
    if len(options) > 26: 
        raise ValueError('Cannot have a menu with more than 26 options')

    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    window = libtcod.console_new(width, height)

    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    index = 1
    for option in options:
        render_func(option, index, window, y)
        index += 1
        y += 1

    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def shop_menu(con, player, shop, screen_width, screen_height):
    menu(con, shop.get_message(), shop.options, 50, screen_width,
         screen_height, render_func=render_shopoption)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty']
    else:
        options = []
        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append(' OFF-HAND: %s' % item.name)
            if player.equipment.off_hand == item:
                options.append('MAIN-HAND: %s' % item.name)
            else:
                options.append(item.name)
    menu(con, header, options, inventory_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def help_menu(con, screen_width):
    window = libtcod.console_new(screen_width, 50)
    window.draw_frame(0, 2, screen_width, 30, "Instructions", True,
                      libtcod.white, libtcod.black)
    libtcod.console_set_default_foreground(window, libtcod.white)
    window.vline(int(screen_width/2)-1, 3, 25)

    col_size = int(screen_width/2)

    col_a = 5
    col_b = col_size+2

    line = 4
    explained(window, " ", "KEYBINDING", col_a, line, libtcod.white,
              libtcod.light_yellow, int(screen_width/2))
    line += 1
    explained(window, "W", ": Move Up", col_a, line, libtcod.light_yellow,
              libtcod.white, col_size)
    line += 1
    explained(window, "A", ": Move Left", col_a, line, libtcod.light_yellow,
              libtcod.white, col_size)
    line += 1
    explained(window, "S", ": Move Down", col_a, line, libtcod.light_yellow,
              libtcod.white, col_size)
    line += 1
    explained(window, "D", ": Move Right", col_a, line, libtcod.light_yellow,
              libtcod.white, col_size)
    line += 1
    explained_longer(window, "1-4", ": Use active tomes", 3, line, libtcod.light_yellow,
              libtcod.white, col_size, 3)

    line += 1
    explained_longer(window, "SPACE", ": Take stairs", 1, line, libtcod.light_yellow,
              libtcod.white, col_size, 5)
    line += 1
    explained_longer(window, "ENTER", ": Take stairs", 1, line, libtcod.light_yellow,
              libtcod.white, col_size, 5)
    line += 1
    explained_longer(window, "MOUSE", ": Aim target spell", 1, line, libtcod.light_yellow,
              libtcod.white, col_size, 5)
    line += 1
    explained(window, "?", ": See this window", col_a, line, libtcod.light_yellow,
              libtcod.white, col_size)

    line += 2
    explained(window, " ", "INTERACT",
              col_a, line, libtcod.light_grey, libtcod.light_yellow, col_size)
    line += 1
    explained(window, " ", "Move towards objects to interact",
              col_a-3, line, libtcod.light_grey, libtcod.white, col_size)
    line += 1
    explained(window, " ", " - Pick up item",
              col_a-3, line, libtcod.light_grey, libtcod.light_grey, col_size)
    line += 1
    explained(window, " ", " - Attack monster",
              col_a-3, line, libtcod.light_grey, libtcod.light_grey, col_size)
    line += 1
    explained(window, " ", " - Browse shop",
              col_a-3, line, libtcod.light_grey, libtcod.light_grey, col_size)
    line += 1
    explained(window, " ", " - Open chest",
              col_a-3, line, libtcod.light_grey, libtcod.light_grey, col_size)

    line += 2
    explained(window, "!", " Try to survive as many",
              col_a-3, line, libtcod.red, libtcod.white, col_size)
    line += 1
    explained(window, " ", "  levels as possible",
              col_a-3, line, libtcod.red, libtcod.white, col_size)
    line += 1
    explained(window, "!", " Boss every 7 levels",
              col_a-3, line, libtcod.red, libtcod.white, col_size)


    line = 4
    explained(window, " ", "ACTIVE TOMES:", col_b, line, libtcod.white,
              libtcod.light_yellow, int(screen_width/2))
    line += 1
    explained(window, " ", "Found around the map", col_b, line, libtcod.white,
              libtcod.light_grey, int(screen_width/2))
    line += 1

    explained(window, "#", "Healing Tome", col_b, line, libtcod.violet,
              libtcod.white, int(screen_width/2))
    line += 1
    explained(window, "#", "Magic Missile Tome", col_b, line, libtcod.light_cyan,
              libtcod.white, int(screen_width/2))
    line += 1
    explained(window, "#", "Paralysis Tome", col_b, line, libtcod.pink,
              libtcod.white, int(screen_width/2))
    line += 1
    explained(window, "#", "Fireball Tome", col_b, line, libtcod.red,
              libtcod.white, int(screen_width/2))
    line += 2

    explained(window, " ", "PASSIVE TOMES", col_b, line, libtcod.white,
              libtcod.light_yellow, int(screen_width/2))
    line += 1
    explained(window, " ", "Bought at the shopkeeper", col_b, line, libtcod.white,
              libtcod.light_grey, int(screen_width/2))
    line += 1
    explained(window, " ", "Strength", col_b, line, libtcod.white,
              libtcod.white, int(screen_width/2))
    line += 1
    explained(window, " ", "Defense", col_b, line, libtcod.white,
              libtcod.white, int(screen_width/2))
    line += 1
    explained(window, " ", "Vitality", col_b, line, libtcod.pink,
              libtcod.white, int(screen_width/2))
    line += 1
    explained(window, " ", "Magic Power", col_b, line, libtcod.red,
              libtcod.white, int(screen_width/2))
    line += 2

    explained(window, " ", "INTERACTIVE ITEMS", col_b, line, libtcod.white,
              libtcod.light_yellow, int(screen_width/2))
    line += 1
    explained(window, " ", "Found around the map", col_b, line, libtcod.white,
              libtcod.light_grey, int(screen_width/2))
    line += 1
    explained(window, "C", "Chest", col_b, line, libtcod.darker_orange,
              libtcod.white, int(screen_width/2))
    line += 1
    explained(window, ">", "Stairs", col_b, line, libtcod.white,
              libtcod.white, int(screen_width/2))
    line += 1
    explained(window, "@", "Shopkeeper", col_b, line, libtcod.blue,
              libtcod.white, int(screen_width/2))

    window.print_box(int((screen_width/2)-15), 29, 30, 1, "Press any key to start",
                     libtcod.light_yellow, libtcod.black,
                     libtcod.BKGND_NONE, libtcod.CENTER)

    libtcod.console_blit(window, 0, 0, screen_width, 32, 0, 0, 7, 1.0, 0.9)


def explained_longer(con, key, value, x, y, key_color, value_color, area_width, key_width):
    libtcod.console_set_default_foreground(con, key_color)
    libtcod.console_print_ex(con, x, y, libtcod.BKGND_NONE, libtcod.LEFT, key)
    libtcod.console_set_default_foreground(con, value_color)
    libtcod.console_print_ex(con, x+key_width, y, libtcod.BKGND_NONE, libtcod.LEFT, value)


def explained(con, key, value, x, y, key_color, value_color, area_width):
    explained_longer(con, key, value, x, y, key_color, value_color, area_width, 1)


def key_value(con, key, value, x, y, key_color, value_color, area_width):
    con.print_box(x, y, int(area_width/2)-1, 1, key, key_color, libtcod.black, libtcod.BKGND_NONE, libtcod.RIGHT)
    libtcod.console_set_default_foreground(con, value_color)
    libtcod.console_print_ex(con, int(area_width/2), y, libtcod.BKGND_NONE, libtcod.LEFT, value)

def stats_key_value(con, key, value, y, value_color, area_width):
    con.print_box(0, 3+y, int(area_width/2)-1, 1, key, libtcod.white, libtcod.black, libtcod.BKGND_NONE, libtcod.RIGHT)
    libtcod.console_set_default_foreground(con, value_color)
    libtcod.console_print_ex(con, int(area_width/2), 3+y, libtcod.BKGND_NONE, libtcod.LEFT, value)

def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'Dragons & Dungeons')

    menu(con, '', ['Play a new game', 'Quit'], 24, screen_width, screen_height)

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = [
        'CON (+20HP, from %s)' % player.fighter.max_hp,
        'STR (+1 Attack, from %s)' % player.fighter.power,
        'AGI (+1 Defense, from %s)' % player.fighter.defense
    ]
    menu(con, header, options, menu_width, screen_width, screen_height)

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '%s: %i/%i' % (name, value, maximum))

