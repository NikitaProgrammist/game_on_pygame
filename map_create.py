from create_labirint import Maze
from constants import *
import pygame
maze_map = Maze(20, 30)
maze_map.generate()
matrix_map = maze_map.to_list_representation()
WORLD_WIDTH = len(matrix_map[0]) * TILE_SIZE
WORLD_HEIGHT = len(matrix_map) * TILE_SIZE
world_map = {}
mini_map = set()
collision_walls = []
wall_types = {1: 1, 2: 2, 3: 3, 4: 4}
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            position = (i * TILE_SIZE, j * TILE_SIZE)
            mini_map.add((i * MAP_TILE_SIZE, j * MAP_TILE_SIZE))
            collision_walls.append(pygame.Rect(*position, TILE_SIZE, TILE_SIZE))
            world_map[position] = wall_types.get(char, 1)
