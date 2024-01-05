from player import Player
from sprites import *
from ray_casting import ray_casting
from drawing import Drawing
from menu import *
sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc)
sc_map = pygame.Surface(((2 * a + 1) * MAP_TILE_SIZE, (2 * a + 1) * MAP_TILE_SIZE))
mini_map_enabled = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYUP and event.key == pygame.K_q:
            mini_map_enabled = not mini_map_enabled

    player.movement()

    sc.fill((0, 0, 0))
    drawing.background(player.angle)

    walls = ray_casting(player.pos, player.angle, drawing.textures, sc)
    objects = [obj.object_locate(player) for obj in sprites.list_of_objects]
    drawing.world(walls + objects)

    drawing.fps(clock)

    if mini_map_enabled:
        drawing.mini_map(player, sc_map)

    pygame.display.flip()
    clock.tick(60)