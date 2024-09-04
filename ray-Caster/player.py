from setings import *
import math
import pygame
class Player:
    def __init__(self):
        self.x = window_widht/2
        self.y = window_height/2
        self.radius = 6
        self.a = math.radians(90)
        self.rotation_speed = math.radians(2)
        self.movespeed = 2.5
        self.turnDirection = 0
        self.walfDirection = 0

    def update(self):
        keys = pygame.key.get_pressed()

        self.turnDirection = 0
        self.walfDirection = 0

        if keys[pygame.K_LEFT]:
            self.turnDirection = 1
        if keys[pygame.K_RIGHT]:
            self.turnDirection = -1

        if keys[pygame.K_UP]:
            self.walfDirection = 1
        if keys[pygame.K_DOWN]:
            self.walfDirection = -1

        self.a += self.rotation_speed * self.turnDirection

        MoveStep = self.walfDirection * self.movespeed

        self.x += MoveStep * math.cos(self.a)
        self.y += MoveStep * math.sin(self.a) 

    def remder(self,screen):
        pygame.draw.circle(screen, (255,0,0), (self.x,self.y), self.radius)

        pygame.draw.line(screen,(0,0,255),(self.x,self.y), ( self.x+math.cos(self.a)*50, self.y+math.sin(self.a)*50 ))
