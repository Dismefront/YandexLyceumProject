import pygame
from random import randint


hud_1 = None
hud_2 = None
hud_3 = None
hud_4 = None
patHouseSprite = None
spongeHouseSprite = None
knights = list()
kgroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
blockscount = randint(8, 15)