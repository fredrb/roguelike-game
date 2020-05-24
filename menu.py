import tcod as libtcod

def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options')

    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    window = libtcod.console_new(width, height)

    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    index = 1
    for option_text in options:
        text = '(' + str(index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        index += 1

    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def shop_menu(con, player, shop, screen_width, screen_height):
    options = [opt.text for opt in shop.options]
    menu(con, shop.get_message(), options, 50, screen_width, screen_height)

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
    con.draw_frame(0, 2, screen_width, 30, "Instructions", True, libtcod.white, libtcod.dark_grey)
    libtcod.console_set_default_foreground(con, libtcod.white)
    con.vline(int(screen_width/2)-1, 3, 40)

    explained(con, " ", "ACTIVE TOMES:", 1, 3, libtcod.white, libtcod.light_grey, int(screen_width/2))
    explained(con, "#", "Healing Tome", 1, 4, libtcod.violet, libtcod.white, int(screen_width/2))
    explained(con, "#", "Magic Missile Tome", 1, 5, libtcod.light_cyan, libtcod.white, int(screen_width/2))
    explained(con, "#", "Paralysis Tome", 1, 6, libtcod.pink, libtcod.white, int(screen_width/2))
    explained(con, "#", "Fireball Tome", 1, 7, libtcod.red, libtcod.white, int(screen_width/2))

    explained(con, " ", "PASSIVE TOMES", 1, 9, libtcod.white, libtcod.light_grey, int(screen_width/2))
    explained(con, " ", "Strength", 1, 10, libtcod.white, libtcod.white, int(screen_width/2))
    explained(con, " ", "Defense", 1, 11, libtcod.white, libtcod.white, int(screen_width/2))
    explained(con, " ", "Vitality", 1, 12, libtcod.pink, libtcod.white, int(screen_width/2))
    explained(con, " ", "Magic Power", 1, 13, libtcod.red, libtcod.white, int(screen_width/2))

    explained(con, " ", "INTERACTIVE ITEMS", 1, 15, libtcod.white, libtcod.light_grey, int(screen_width/2))
    explained(con, "C", "Chest", 1, 16, libtcod.darker_orange, libtcod.white, int(screen_width/2))
    explained(con, ">", "Stairs", 1, 17, libtcod.white, libtcod.white, int(screen_width/2))
    explained(con, "@", "Shopkeeper", 1, 19, libtcod.blue, libtcod.white, int(screen_width/2))



def explained(con, key, value, x, y, key_color, value_color, area_width):
    libtcod.console_set_default_foreground(con, key_color)
    libtcod.console_print_ex(con, x, y, libtcod.BKGND_NONE, libtcod.LEFT, key)
    libtcod.console_set_default_foreground(con, value_color)
    libtcod.console_print_ex(con, x+1, y, libtcod.BKGND_NONE, libtcod.LEFT, value)


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

