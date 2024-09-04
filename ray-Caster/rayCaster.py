from setings import *
from ray import Ray
from map import Map
import pygame
map = Map()
class RayCaster:
    def __init__(self, palyer):
        self.palyer = palyer
        self.rays = []



    def CastAll(self):
        self.rays = []
        RayAngle = (self.palyer.a - FOV / 2)
        for i in range(NUM_RAYS):
            ray = Ray(RayAngle, self.palyer, map)
            ray.cast()
            self.rays.append(ray)
            RayAngle += FOV / NUM_RAYS



    def render(self, screen):
        i = 0 
        for ray in self.rays:

            line_height = (32 / ray.distance)* 415

            draw_begin = (window_height/2) - (line_height / 2)
            drew_end = line_height
            pygame.draw.rect(screen,(0,255,0),(i*RES, draw_begin, RES, drew_end))
            i +=1
            


