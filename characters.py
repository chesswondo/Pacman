from abc import ABC, abstractmethod
from typing import Tuple
import random
import pygame
import numpy as np
from utils import *

class Character(ABC):
    '''Base class for all characters in the game.'''
    def __init__(self,
                 grid: np.ndarray,
                 field_size: Tuple[int, int],
                 map_width: int,
                 map_height: int,
                 image_path: str) -> None:
        
        self._grid = grid
        self._field_size = field_size
        self._map_width = map_width
        self._map_height = map_height
        self._image_path = image_path

        self.image = self._load_image()
        self.x, self.y = self._initialize_field()


    @abstractmethod
    def _load_image(self):
        '''Loads and scales image.'''

    def _initialize_field(self) -> Tuple[int, int]:
        while(True):
            x = random.randrange(self._map_width)
            y = random.randrange(self._map_height)
            if self._grid[x][y] == 0:
                return (x, y)


class Pacman(Character):
    '''Class for the Pacman.'''
    def __init__(self,
                 grid: np.ndarray,
                 field_size: Tuple[int, int],
                 map_width: int,
                 map_height: int,
                 image_path: str) -> None:
        
        super().__init__(grid,
                        field_size,
                        map_width,
                        map_height,
                        image_path)
        
    def _load_image(self):
        player_image = pygame.image.load(self._image_path)
        player_image = pygame.transform.scale(player_image, self._field_size)
        return player_image
    
    def make_move(self, command: str) -> None:
        if command == 'left':
            if is_left_possible(self.x, self.y, self._map_width, self._map_height, self._grid):
                self.x -= 1
        if command == 'right':
            if is_right_possible(self.x, self.y, self._map_width, self._map_height, self._grid):
                self.x += 1
        if command == 'up':
            if is_up_possible(self.x, self.y, self._map_width, self._map_height, self._grid):
                self.y -= 1
        if command == 'down':
            if is_down_possible(self.x, self.y, self._map_width, self._map_height, self._grid):
                self.y += 1
    

class Dot(Character):
    '''Class for dots.'''
    def __init__(self,
                 grid: np.ndarray,
                 field_size: Tuple[int, int],
                 map_width: int,
                 map_height: int,
                 image_path: str) -> None:
        
        super().__init__(grid,
                        field_size,
                        map_width,
                        map_height,
                        image_path)
        
    def _load_image(self):
        dot_image = pygame.image.load(self._image_path)
        dot_image = pygame.transform.scale(dot_image, tuple(size//2 for size in self._field_size))
        return dot_image
    

class Ghost(Character):
    '''Class for ghosts.'''
    def __init__(self,
                 grid: np.ndarray,
                 field_size: Tuple[int, int],
                 map_width: int,
                 map_height: int,
                 image_path: str) -> None:
        
        super().__init__(grid,
                        field_size,
                        map_width,
                        map_height,
                        image_path)
        
    def _load_image(self):
        ghost_image = pygame.image.load(self._image_path)
        ghost_image = pygame.transform.scale(ghost_image, self._field_size)
        return ghost_image
    
    def make_move(self) -> None:
        possible_ghost_ways = []

        if is_up_possible(self.x, self.y, self._map_width, self._map_height, self._grid):
            possible_ghost_ways.append('up')
        if is_down_possible(self.x, self.y, self._map_width, self._map_height, self._grid):
            possible_ghost_ways.append('down')
        if is_left_possible(self.x, self.y, self._map_width, self._map_height, self._grid):
            possible_ghost_ways.append('left')
        if is_right_possible(self.x, self.y, self._map_width, self._map_height, self._grid):
            possible_ghost_ways.append('right')

        direction = random.choice(possible_ghost_ways)
        if direction == 'up':
            self.y -= 1
        if direction == 'down':
            self.y += 1
        if direction == 'left':
            self.x -= 1
        if direction == 'right':
            self.x += 1