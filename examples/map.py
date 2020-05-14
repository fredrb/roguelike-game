import tcod

tcod.console_set_custom_font('../arial10x10.png', 
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

def screen_map(game_map, name):
    colors = {
        'dark_wall': tcod.Color(18, 18, 20),
        'dark_ground': tcod.Color(50, 50, 50),
        'light_wall': tcod.Color(130, 130, 130),
        'light_ground': tcod.Color(200, 200, 200)
    }

    with tcod.console_init_root(25, 25, name, False, None, 'C', True) as root:
        while True:
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()

            game_map.compute_fov(2, 3, 10, light_walls=True, algorithm=1)
            for y in range(game_map.height):
                for x in range(game_map.width):
                    if game_map.fov[y,x]:
                        if game_map.walkable[y,x]:
                            tcod.console_set_char_background(root, x, y, colors.get('light_ground'), tcod.BKGND_SET)
                        else:
                            tcod.console_set_char_background(root, x, y, colors.get('light_wall'), tcod.BKGND_SET)
                    else:
                        if game_map.walkable[y,x]:
                            tcod.console_set_char_background(root, x, y, colors.get('dark_ground'), tcod.BKGND_SET)
                        else:
                            tcod.console_set_char_background(root, x, y, colors.get('dark_wall'), tcod.BKGND_SET)

            tcod.console_blit(root, 0, 0, 25, 25, 0, 0, 0)
            tcod.console_flush()


if __name__ == '__main__':
    game_map = tcod.map.Map(25, 25)

    game_map.walkable[:] = False
    game_map.transparent[:] = False

    game_map.walkable[2:6,0] = True
    game_map.walkable[2:6,1] = True
    game_map.walkable[2:6,2] = True
    game_map.walkable[2:6,3] = True
    game_map.walkable[3,4] = True
    game_map.walkable[3,5] = True
    game_map.walkable[3,6] = True
    game_map.walkable[3,7] = True
    game_map.walkable[3,8] = True
    game_map.walkable[2:6,8] = True
    game_map.walkable[2:6,9] = True
    game_map.walkable[2:6,10] = True
    game_map.walkable[2:6,11] = True
    game_map.transparent[2:6,0] = True
    game_map.transparent[2:6,1] = True
    game_map.transparent[2:6,2] = True
    game_map.transparent[2:6,3] = True
    game_map.transparent[3,4] = True
    game_map.transparent[3,5] = True
    game_map.transparent[3,6] = True
    game_map.transparent[3,7] = True
    game_map.transparent[3,8] = True
    game_map.transparent[2:6,8] = True
    game_map.transparent[2:6,9] = True
    game_map.transparent[2:6,10] = True
    game_map.transparent[2:6,11] = True

    screen_map(game_map, 'Example 1')
    
