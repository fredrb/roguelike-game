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

def city_bg(con, background_image, screen_width, screen_height):
    con.draw_frame(1, 1, screen_width - 2, screen_height - 2, "CITY OF METANO", True, libtcod.white, libtcod.black)
    libtcod.console_set_default_foreground(0, libtcod.light_grey)
    con.draw_frame(1, 1, 17, 8, "PURSE")
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    con.print_(2, 3, "Gold") 
    libtcod.console_set_default_foreground(0, libtcod.light_grey)
    con.print_(2, 4, "Silver") 
    libtcod.console_set_default_foreground(0, libtcod.Color(190, 150, 100))
    con.print_(2, 5, "Copper") 

    libtcod.console_set_default_foreground(0, libtcod.white)
    con.print_(11, 3, "23") 
    

def _city_bg(con, background_image, screen_width, screen_height):
    con.draw_frame(1, 1, screen_width - 2, screen_height - 2, "CITY OF METANO", True, libtcod.white, libtcod.black)
    libtcod.console_set_default_foreground(0, libtcod.light_grey)
    con.vline(int(screen_width/2), 4, screen_height - 8)
    con.draw_frame(1, 1, 20, 10)
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)

    con.print_(2, 2, "SHARDS") 
    con.print_(12, 2, "SLOTS") 

    libtcod.console_set_default_foreground(0, libtcod.white)
    con.print_(3, 4, "A")
    con.print_(3, 5, "B")
    con.print_(3, 6, "C")
    con.print_(3, 7, "D")
    con.print_(3, 8, "E")

    con.print_(5, 4, "%s" % ("x0"))
    con.print_(5, 5, "%s" % ("x0"))
    con.print_(5, 6, "%s" % ("x0"))
    con.print_(5, 7, "%s" % ("x0"))
    con.print_(5, 8, "%s" % ("x0"))

    con.draw_rect(12, 4, 1, 1, 0, libtcod.white, libtcod.grey)

    
    con.print_(int(screen_width/2)+2, 4, "AA")
    con.print_(int(screen_width/2)+2, 5, "AB")

    #con.print_box(int(screen_width/2)+14, 4, 8, 1, "Craft", libtcod.white, libtcod.blue)
    #con.print_box(int(screen_width/2)+14, 5, 8, 1, "Craft", libtcod.white, libtcod.blue)

    #libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    #con.print_(int(screen_width/4)-2, 4, "SHARDS")
    #con.print_(int(screen_width/4)-2, int(screen_height/2), "SLOTS")

    #con.print_(int(screen_width/2)+int(screen_width/4)-2, 4, "RECIPES")

def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)
    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'KENYA SURVIVAL')
    #libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
    #                         '')

    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)

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

