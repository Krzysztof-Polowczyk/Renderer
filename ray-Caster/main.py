import pygame
from setings import *
from map import Map
from player import Player
from rayCaster import RayCaster
clock = pygame.time.Clock()
map = Map()
player = Player()
rayCaster = RayCaster(player)
SCREEN = pygame.display.set_mode((window_widht,window_height))

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()
    rayCaster.CastAll()
    SCREEN.fill((0,0,0))
    player.update()
    rayCaster.render(SCREEN)

    pygame.display.update()