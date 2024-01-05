from constants import *
from collections import deque


def load_sprite_images(base_path, count):
    return [pygame.image.load(f'{base_path}/{i}.png').convert_alpha() for i in range(count)]


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
        }

        self.list_of_objects = [
        ]

    def create_sprite_parameters(self, path, anim_count, viewing_angles, shift, scale, anim_dist, anim_speed, blocked):
        sprite = load_sprite_images(f'{path}/base', 1)[0]
        animation = deque(load_sprite_images(f'{path}/anim', anim_count))

        parameters = {
            'sprite': sprite,
            'shift': shift,
            'scale': scale,
            'animation': animation,
            'animation_dist': anim_dist,
            'animation_speed': anim_speed,
            'blocked': blocked,
        }

        if viewing_angles:
            parameters['sprite'] = load_sprite_images(f'{path}/base', 8)
            parameters['viewing_angles'] = True
            parameters['sprite_positions'] = {angle: sprite for angle, sprite in
                                              zip(range(0, 360, 45), parameters['sprite'])}
        else:
            parameters['viewing_angles'] = False

        return parameters


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.side = 30
        self.animation_count = 0
        self.x, self.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        self.pos = self.x - self.side // 2, self.y - self.side // 2

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}
        else:
            self.sprite_angles = None
            self.sprite_positions = None

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += 2 * math.pi

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), 2 * HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift
            if self.viewing_angles:
                if theta < 0:
                    theta += 2 * math.pi
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return distance_to_sprite, sprite, sprite_pos
        else:
            return (False,)
