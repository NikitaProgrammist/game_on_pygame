from map_create import matrix_map
from player import Player
from sprites import *
from ray_casting import ray_casting
from drawing import Drawing
sc_map = pygame.Surface((len(matrix_map[0]) * MAP_TILE_SIZE, len(matrix_map) * MAP_TILE_SIZE))
sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map)

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
        drawing.mini_map(player)

    pygame.display.flip()
    clock.tick(60)