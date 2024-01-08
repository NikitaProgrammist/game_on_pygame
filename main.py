from player import Player
from ray_casting import ray_casting
from drawing import DrawMainScreen
from create_labirint import *
from buttons import Button
start_game(sc)
a, b, tex, matrix_map, WORLD_WIDTH, WORLD_HEIGHT = create_labirint()
clock = pygame.time.Clock()
player = Player()
draw = DrawMainScreen()
sc_map = pygame.Surface(((2 * a + 1) * MAP_TILE_SIZE, (2 * b + 1) * MAP_TILE_SIZE))
mini_map_enabled = True
button = Button(sc.get_size()[0] - 65, 0, 65, 65, pygame.font.Font(None, 30), '...')
start_ticks = pygame.time.get_ticks()
while True:
    pygame.display.set_caption('затерянный в лабиринте')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            stop_time = pygame.time.get_ticks()
            flag_1 = menu(sc)
            seconds = pygame.time.get_ticks() - stop_time
            start_ticks += seconds
            if flag_1:
                a, b, tex, matrix_map, WORLD_WIDTH, WORLD_HEIGHT = create_labirint()
                clock = pygame.time.Clock()
                sc_map = pygame.Surface(((2 * a + 1) * MAP_TILE_SIZE, (2 * b + 1) * MAP_TILE_SIZE))
                start_ticks = pygame.time.get_ticks()
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            mini_map_enabled = not mini_map_enabled
    player.movement()
    sc.fill((0, 0, 0))
    draw.background(player.angle, tex)
    walls = ray_casting(player.pos, player.angle, draw.textures, WORLD_WIDTH, WORLD_HEIGHT)
    draw.world(walls)
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    draw.timer(minutes, seconds)
    draw.fps(clock)
    game_flag = draw.mini_map(player, sc_map, mini_map_enabled)
    if game_flag:
        new_game_flag = win(sc, minutes, seconds, a, b, tex)
        if new_game_flag:
            pygame.mouse.set_visible(True)
            start_game(sc)
            a, b, tex, matrix_map, WORLD_WIDTH, WORLD_HEIGHT = create_labirint()
            clock = pygame.time.Clock()
            sc_map = pygame.Surface(((2 * a + 1) * MAP_TILE_SIZE, (2 * b + 1) * MAP_TILE_SIZE))
            start_ticks = pygame.time.get_ticks()
    flag = button.process()
    if flag:
        stop_time = pygame.time.get_ticks()
        flag_1 = menu(sc)
        seconds = pygame.time.get_ticks() - stop_time
        start_ticks += seconds
        if flag_1:
            a, b, tex, matrix_map, WORLD_WIDTH, WORLD_HEIGHT = create_labirint()
            clock = pygame.time.Clock()
            sc_map = pygame.Surface(((2 * a + 1) * MAP_TILE_SIZE, (2 * b + 1) * MAP_TILE_SIZE))
            start_ticks = pygame.time.get_ticks()
    pygame.display.flip()
    clock.tick(60)
