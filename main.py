import pygame
import json
import os
from pygame import *
from Utilities.load_image import load_image
from Classes.PyMain import PyMain
from Classes.Player import Player
from Classes.StaticObject import StaticObject

FPS = 30
WIN_WIDTH = 700
WIN_HEIGHT = 600
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = (0, 0, 0)

pygame.init()

f = open(os.path.join("Maps", "test_map_2.json"))
json_map = json.load(f)
f.close()
f = open(os.path.join("Descriptions", "objects.json"))
description = json.load(f)
f.close()

main = PyMain(json_map, description, width=WIN_WIDTH, height=WIN_HEIGHT)

hero = Player(main.start_pos[0], main.start_pos[1])

main.mainloop(hero, fps=FPS)  # Главный цикл
