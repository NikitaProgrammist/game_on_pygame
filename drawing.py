from constants import *
from create_labirint import mini_map


class DrawMainScreen:
    def __init__(self, sc):
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', 36, True)
        self.textures = self.load_textures()
        for i in self.textures:
            if 'S' in str(i):
                self.textures[i] = pygame.transform.scale(self.textures[i],
                                                          (sc.get_size()[0], sc.get_size()[0] *
                                                           self.textures[i].get_size()[1] /
                                                           self.textures[i].get_size()[0]))

    def load_textures(self):
        textures = {f'S{i}': f'img/sky{i}.png' for i in range(1, 9)}
        textures.update({i: f'img/wall{i}.png' for i in range(1, 9)})
        textures.update({i: f'img/exit{i - 10}.png' for i in range(11, 19)})
        return {key: pygame.image.load(path).convert() for key, path in textures.items()}

    def background(self, angle, tex):
        sky_offset = -10 * math.degrees(angle) % WIDTH
        for offset in (sky_offset - WIDTH, sky_offset, sky_offset + WIDTH):
            self.sc.blit(self.textures[f'S{tex}'], (offset, 0))
        pygame.draw.rect(self.sc, (40, 40, 40), (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, walls):
        for obj in sorted(walls, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def timer(self, minutes, seconds):
        timer_text = self.font.render(f"{minutes}: {seconds:02}", True, (0, 0, 0))
        self.sc.blit(timer_text, (self.sc.get_size()[0] // 2 - 25, 65))

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, (255, 150, 0))
        self.sc.blit(render, (WIDTH - 65, HEIGHT - 65))

    def mini_map(self, player, sc_map, mini_map_enabled):
        sc_map.fill((0, 0, 0))
        map_x, map_y = int(player.x // MAP_SCALE), int(player.y // MAP_SCALE)
        direction = (map_x + 10 * math.cos(player.angle), map_y + 10 * math.sin(player.angle))
        pygame.draw.line(sc_map, (255, 255, 0), (map_x, map_y), direction, 2)
        pygame.draw.circle(sc_map, (255, 0, 0), (map_x, map_y), 5)
        for x, y in mini_map:
            pygame.draw.rect(sc_map, (100, 65, 25), (x, y, MAP_TILE_SIZE, MAP_TILE_SIZE))
        rect = pygame.Rect((sc_map.get_size()[0] - 2 * MAP_TILE_SIZE, sc_map.get_size()[1] - MAP_TILE_SIZE, MAP_TILE_SIZE, MAP_TILE_SIZE))
        pygame.draw.rect(sc_map, (255, 215, 0), rect)
        if mini_map_enabled:
            self.sc.blit(sc_map, (0, 0), (map_x - 50, map_y - 50, map_x + 150, map_y + 150))
        if rect.collidepoint(direction):
            return True
