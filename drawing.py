from constants import *
from create_labirint import mini_map, tex


class Drawing:
    def __init__(self, sc):
        self.sc = sc
        self.text = ''
        self.tick = 30
        self.finput = False
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = self.load_textures()
        for i in self.textures:
            if 'S' in str(i):
                self.textures[i] = pygame.transform.scale(self.textures[i], (sc.get_size()[0], sc.get_size()[0] * self.textures[i].get_size()[1] / self.textures[i].get_size()[0]))

    def load_textures(self):
        textures = {f'S{i}': f'img/sky{i}.png' for i in range(1, 5)}
        textures.update({i: f'img/wall{i + 2}.png' for i in range(1, 5)})
        return {key: pygame.image.load(path).convert() for key, path in textures.items()}

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % self.sc.get_size()[0]
        for offset in (sky_offset - self.sc.get_size()[0], sky_offset, sky_offset + self.sc.get_size()[0]):
            self.sc.blit(self.textures[f'S{tex}'], (offset, 0))
        pygame.draw.rect(self.sc, (40, 40, 40), (0, self.sc.get_size()[1] // 2, self.sc.get_size()[0], self.sc.get_size()[1] // 2))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, (object_pos[0] * self.sc.get_size()[0] / WIDTH, object_pos[1] * self.sc.get_size()[1] / HEIGHT))

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, (255, 150, 0))
        self.sc.blit(render, (self.sc.get_size()[0] - 65, 5))

    def mini_map(self, player, sc_map):
        sc_map.fill((0, 0, 0))
        map_x, map_y = int(player.x // MAP_SCALE), int(player.y // MAP_SCALE)
        direction = (map_x + 10 * math.cos(player.angle), map_y + 10 * math.sin(player.angle))
        pygame.draw.line(sc_map, (255, 255, 0), (map_x, map_y), direction, 2)
        pygame.draw.circle(sc_map, (255, 0, 0), (map_x, map_y), 5)
        for x, y in mini_map:
            pygame.draw.rect(sc_map, (100, 65, 25), (x, y, MAP_TILE_SIZE, MAP_TILE_SIZE))
        self.sc.blit(sc_map, (0, 0), area=(map_x - 50, map_y - 50, map_x + 150, map_y + 150))
