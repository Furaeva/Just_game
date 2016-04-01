import tkinter
from tkinter import *
import pygame
import os
import platform
import threading


def objects_window():
    root = Tk()
    embed = Frame(root, width=300, height=300)
    embed.grid(row=0, column=2)
    # playpausebutton = Button(root, command=playpause, text="Play/Pause")
    # playpausebutton.grid(row=1, column=2)
    root.update()

    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    if platform == 'windows':
        os.environ['SDL_VIDEODRIVER'] = 'windib'

    pygame.display.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
        root.update()


def walls_window():
    win = Tk()
    emb = Frame(win, width=300, height=300)
    emb.grid(row=0, column=2)
    # playpausebutton = Button(root, command=playpause, text="Play/Pause")
    # playpausebutton.grid(row=1, column=2)
    win.update()

    os.environ['SDL_WINDOWID'] = str(emb.winfo_id())
    if platform == 'windows':
        os.environ['SDL_VIDEODRIVER'] = 'windib'

    pygame.display.init()
    scr = pygame.display.set_mode((300, 300))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
        win.update()
