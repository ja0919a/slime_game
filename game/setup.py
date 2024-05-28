import pygame
import os
from . import tool

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Slime Vs Dragon")
pygame.display.set_icon(pygame.image.load("./resource/image/slime.png"))
screen.fill((0,0,0))
fonts_36=tool.load_font("./resource/font", 36)
img_list=tool.load_image("./resource/image")
forest_img = img_list["forest"]
slime_imgs = [img_list["slime-"+str(i)] for i in range(1,6)]
dragon_imgs = [img_list["dragon-"+str(i)] for i in range(1,5)]
explode_imgs = [img_list["explode-"+str(i)] for i in range(1,9)]