from random import choice
from constants import *
from menu import *


class Maze:
    def __init__(self, w, h):
        self.cols, self.rows = w, h
        self.grid = [[{'top': True, 'right': True, 'bottom': True, 'left': True, 'visited': False}
                      for _ in range(self.cols)] for _ in range(self.rows)]

    def remove_walls(self, x1, y1, x2, y2):
        dx = x1 - x2
        dy = y1 - y2
        if dx == 1:
            self.grid[y1][x1]['left'] = False
            self.grid[y2][x2]['right'] = False
        elif dx == -1:
            self.grid[y1][x1]['right'] = False
            self.grid[y2][x2]['left'] = False
        if dy == 1:
            self.grid[y1][x1]['top'] = False
            self.grid[y2][x2]['bottom'] = False
        elif dy == -1:
            self.grid[y1][x1]['bottom'] = False
            self.grid[y2][x2]['top'] = False

    def check_neighbors(self, x, y):
        neighbors = []
        directions = [('top', 0, -1), ('right', 1, 0), ('bottom', 0, 1), ('left', -1, 0)]
        for direction, dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows and not self.grid[ny][nx]['visited']:
                neighbors.append((nx, ny))
        return choice(neighbors) if neighbors else None

    def generate(self):
        stack = []
        x, y = 0, 0
        self.grid[y][x]['visited'] = True

        while True:
            next_cell = self.check_neighbors(x, y)
            if next_cell:
                next_x, next_y = next_cell
                stack.append((x, y))
                self.remove_walls(x, y, next_x, next_y)
                x, y = next_x, next_y
                self.grid[y][x]['visited'] = True
            elif stack:
                x, y = stack.pop()
            else:
                break

    def to_list_representation(self, tex):
        maze = [[tex for _ in range(self.cols * 2 + 1)] for _ in range(self.rows * 2 + 1)]
        for y in range(self.rows):
            for x in range(self.cols):
                cell_x, cell_y = x * 2 + 1, y * 2 + 1
                maze[cell_y][cell_x] = 0
                if not self.grid[y][x]['top']:
                    maze[cell_y - 1][cell_x] = 0
                if not self.grid[y][x]['right']:
                    maze[cell_y][cell_x + 1] = 0
                if not self.grid[y][x]['bottom']:
                    maze[cell_y + 1][cell_x] = 0
                if not self.grid[y][x]['left']:
                    maze[cell_y][cell_x - 1] = 0
        return maze


world_map = {}
mini_map = set()
collision_walls = []


def create_labirint():
    global world_map, mini_map, collision_walls
    world_map.clear()
    mini_map.clear()
    collision_walls.clear()
    a, b, tex = game_init(sc)
    maze_map = Maze(a, b)
    maze_map.generate()
    matrix_map = maze_map.to_list_representation(tex)
    matrix_map[-1][-2] += 10
    WORLD_WIDTH = len(matrix_map[0]) * TILE_SIZE
    WORLD_HEIGHT = len(matrix_map) * TILE_SIZE
    for j, row in enumerate(matrix_map):
        for i, char in enumerate(row):
            if char:
                position = (i * TILE_SIZE, j * TILE_SIZE)
                mini_map.add((i * MAP_TILE_SIZE, j * MAP_TILE_SIZE))
                collision_walls.append(pygame.Rect(*position, TILE_SIZE, TILE_SIZE))
                world_map[position] = char
    return a, b, tex, matrix_map, WORLD_WIDTH, WORLD_HEIGHT
