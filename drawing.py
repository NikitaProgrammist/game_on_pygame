import pygame
from constants import *
from map_create import mini_map


class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = self.load_textures()

    def load_textures(self):
        textures = {'S': 'img/sky2.png'}
        textures.update({i: f'img/wall{i + 2}.png' for i in range(1, 5)})
        return {key: pygame.image.load(path).convert() for key, path in textures.items()}

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % WIDTH
        for offset in (sky_offset - WIDTH, sky_offset, sky_offset + WIDTH):
            self.sc.blit(self.textures['S'], (offset, 0))
        pygame.draw.rect(self.sc, (40, 40, 40), (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, (255, 150, 0))
        self.sc.blit(render, (WIDTH - 65, 5))

    def mini_map(self, player):
        self.sc_map.fill((0, 0, 0))
        map_x, map_y = int(player.x // MAP_SCALE), int(player.y // MAP_SCALE)
        direction = (map_x + 10 * math.cos(player.angle), map_y + 10 * math.sin(player.angle))
        pygame.draw.line(self.sc_map, (255, 255, 0), (map_x, map_y), direction, 2)
        pygame.draw.circle(self.sc_map, (255, 0, 0), (map_x, map_y), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, (100, 65, 25), (x, y, MAP_TILE_SIZE, MAP_TILE_SIZE))
        self.sc.blit(self.sc_map, (0, 0), area=(map_x - 50, map_y - 50, map_x + 150, map_y + 150))