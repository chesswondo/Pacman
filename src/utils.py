import json

def is_up_possible(object_x, object_y, width, height, grid):
    if object_y == 0:
        return False
    if grid[object_x][object_y-1] == 1:
        return False
    return True

def is_down_possible(object_x, object_y, width, height, grid):
    if object_y == height-1:
        return False
    if grid[object_x][object_y+1] == 1:
        return False
    return True

def is_left_possible(object_x, object_y, width, height, grid):
    if object_x == 0:
        return False
    if grid[object_x-1][object_y] == 1:
        return False
    return True

def is_right_possible(object_x, object_y, width, height, grid):
    if object_x == width-1:
        return False
    if grid[object_x+1][object_y] == 1:
        return False
    return True

def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return json.load(f)