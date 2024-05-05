import pygame
import os
from . import tool

pygame.init()
screen = pygame.display.set_mode((640, 480))
screen.fill((0,0,0))
pygame.mouse.set_visible(False)
fonts_36=tool.load_font("./resource/font", 36)
forest_img = pygame.image.load("./resource/image/forest.png")