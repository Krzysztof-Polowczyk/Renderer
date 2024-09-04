from setings import *
import pygame
import math
class Map:
    def __init__(self):
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def has_wall_at(self, x,y):
        return self.grid[int(y//tile_size)][int(x//tile_size)]
    
    def render(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                tile_x = j * tile_size
                tile_y = i * tile_size
                if self.grid[i][j]:
                    pygame.draw.rect(screen, (40,40,40), (tile_x, tile_y, tile_size-1,tile_size-1))
                else:
                    pygame.draw.rect(screen, (225,225,225), (tile_x, tile_y, tile_size-1,tile_size-1))
                
