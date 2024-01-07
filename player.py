import pygame

from constants import *
from create_labirint import collision_walls


class Player:
    def __init__(self):
        self.position = pygame.math.Vector2((125, 125))
        self.angle = 4 * math.pi / 3
        self.sensitivity = 0.01
        self.move_speed = 2
        self.rotation_speed = 0.02
        self.mouse_move = True
        self.side = 50
        self.rect = pygame.Rect(*self.position, self.side, self.side)
        self.collision_walls = collision_walls

    @property
    def pos(self):
        return self.position

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def detect_collision(self, move_vector):
        next_rect = self.rect.copy()
        next_rect.move_ip(*move_vector)
        hit_indexes = next_rect.collidelistall(self.collision_walls)

        if hit_indexes:
            delta_x, delta_y = self.calculate_collision_delta(next_rect, hit_indexes, move_vector)
            move_vector = self.resolve_collision(delta_x, delta_y, move_vector)

        return move_vector

    def calculate_collision_delta(self, next_rect, hit_indexes, move_vector):
        delta_x, delta_y = 0, 0
        for hit_index in hit_indexes:
            hit_rect = self.collision_walls[hit_index]
            if move_vector.x > 0:
                delta_x += next_rect.right - hit_rect.left
            elif move_vector.x < 0:
                delta_x += hit_rect.right - next_rect.left

            if move_vector.y > 0:
                delta_y += next_rect.bottom - hit_rect.top
            elif move_vector.y < 0:
                delta_y += hit_rect.bottom - next_rect.top

        return delta_x, delta_y

    def resolve_collision(self, delta_x, delta_y, move_vector):
        if abs(delta_x - delta_y) < 10:
            move_vector.x, move_vector.y = 0, 0
        elif delta_x > delta_y:
            move_vector.y = 0
        else:
            move_vector.x = 0

        return move_vector

    def movement(self):
        self.keys_control()
        if self.mouse_move:
            self.mouse_control()
        self.rect.center = self.position
        self.angle %= 2 * math.pi

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()

        move_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]:
            move_vector += self.move_speed * pygame.math.Vector2(cos_a, sin_a)
        if keys[pygame.K_s]:
            move_vector -= self.move_speed * pygame.math.Vector2(cos_a, sin_a)
        if keys[pygame.K_a]:
            move_vector += self.move_speed * pygame.math.Vector2(sin_a, -cos_a)
        if keys[pygame.K_d]:
            move_vector -= self.move_speed * pygame.math.Vector2(sin_a, -cos_a)
        if keys[pygame.K_e]:
            self.move_speed += 4
        else:
            self.move_speed = 2

        corrected_move = self.detect_collision(move_vector)
        self.position += corrected_move

        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed

        self.mouse_move = not keys[pygame.K_LCTRL]
        pygame.mouse.set_visible(not self.mouse_move)

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity
