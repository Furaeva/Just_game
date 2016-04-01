import pygame
from pygame import *
from pgu import gui
from pgu.gui import Menus
fps = 30
init()

screen = display.set_mode((400, 400))

rect_pgu = pygame.Rect(0, 0, 300, 100)

btn_click = gui.Button("Click Me")
btn_ok = gui.Button("Ok")
data = [
        ('File/Save', None, None),
        ('File/New', None, None),
        ('Edit/Copy', None, None),
        ('Edit/Cut', None, None),
        ('Help/About', None, None),
        ('Help/Reference', None, None),
        ]
menu = Menus(data)

table = gui.Table()
table.td(menu)
table.style.align = -1
table.style.valign = -1

app = gui.App()

app.init(widget=table, screen=screen, area=rect_pgu)
clock = time.Clock()
while True:
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        app.event(e)

    dt = clock.tick(fps)
    app.paint()
    display.flip()