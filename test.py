from pygame import *
from Utilities.load_image import load_image
import os
import sys

init()

screen = display.set_mode((600, 600))
sur = load_image("chest.gif")
flo = load_image("flower1.gif")
screen.blit(sur, (20, 20))
screen.blit(flo, (300, 70))

while True:
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
    display.update()
    display.flip()
