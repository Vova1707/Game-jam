import pygame, math, sys, time, end, main
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((1024, 768))
running = 1
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_SPACE: 
                    main.level1()
                if event.key == K_SPACE or event.type == pygame.QUIT:
                    running = 0
    img = pygame.image.load("images/main_menu_image.png")
    screen.blit(img,(0,0))
    pygame.display.flip()
