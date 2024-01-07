from constants import *
from create_labirint import world_map


def mapping(a, b):
    TILE_SIZE = 100
    return (a // TILE_SIZE) * TILE_SIZE, (b // TILE_SIZE) * TILE_SIZE


def ray_casting(player_pos, player_angle, textures, WORLD_WIDTH, WORLD_HEIGHT):
    casted_walls = []
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - HALF_FOV

    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle) or 0.000001
        cos_a = math.cos(cur_angle) or 0.000001

        x, dx = (xm + TILE_SIZE, 1) if cos_a >= 0 else (xm, -1)
        depth_v, texture_v = float('inf'), None
        while 0 <= x < WORLD_WIDTH:
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx * 0.5, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE_SIZE

        y, dy = (ym + TILE_SIZE, 1) if sin_a >= 0 else (ym, -1)
        depth_h, texture_h = float('inf'), None
        while 0 <= y < WORLD_HEIGHT:
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy * 0.5)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE_SIZE

        if depth_v < depth_h:
            depth, offset, texture = depth_v, yv, texture_v
        else:
            depth, offset, texture = depth_h, xh, texture_h

        depth *= math.cos(player_angle - cur_angle)

        depth = max(depth, 0.00001)
        proj_height = min(int(PROJ_COEFF / depth), 5 * HEIGHT)
        offset = int(offset) % TILE_SIZE

        if texture is not None:
            wall_column = textures[texture].subsurface(offset * 12, 0, 12, 1200)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
        else:
            wall_column = pygame.Surface((SCALE, proj_height))  # Handle no texture case

        wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
        casted_walls.append((depth, wall_column, wall_pos))

        cur_angle += DELTA_ANGLE

    return casted_walls
