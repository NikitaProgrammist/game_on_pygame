from player import Player
from sprites import *
from ray_casting import ray_casting
from drawing import Drawing
from create_labirint import *
from buttons import Button

if start_game(sc):
    a, b, tex, matrix_map, WORLD_WIDTH, WORLD_HEIGHT = create_labirint()
else:
    quit()
sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc)
mini_map_enabled = True
font = pygame.font.Font(None, 30)
button = Button(sc.get_size()[0] - 65, 0, 65, 65, font, '...')
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
                sprites = Sprites()
                clock = pygame.time.Clock()
                player = Player(sprites)
                start_ticks = pygame.time.get_ticks()
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            mini_map_enabled = not mini_map_enabled

    player.movement()

    sc.fill((0, 0, 0))
    drawing.background(player.angle, tex)

    walls = ray_casting(player.pos, player.angle, drawing.textures, WORLD_WIDTH, WORLD_HEIGHT)
    objects = [obj.object_locate(player) for obj in sprites.list_of_objects]
    drawing.world(walls + objects)
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    drawing.timer(minutes, seconds)

    drawing.fps(clock)

    if mini_map_enabled:
        sc_map = pygame.Surface(((2 * a + 1) * MAP_TILE_SIZE, (2 * b + 1) * MAP_TILE_SIZE))
        drawing.mini_map(player, sc_map)
    flag = button.process()
    if flag:
        stop_time = pygame.time.get_ticks()
        flag_1 = menu(sc)
        seconds = pygame.time.get_ticks() - stop_time
        start_ticks += seconds
        if flag_1:
            a, b, tex, matrix_map, WORLD_WIDTH, WORLD_HEIGHT = create_labirint()
            sprites = Sprites()
            clock = pygame.time.Clock()
            player = Player(sprites)
            start_ticks = pygame.time.get_ticks()
    pygame.display.flip()
    clock.tick(60)