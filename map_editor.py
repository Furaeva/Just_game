import pygame
import tkinter
import os
import sys
import json
import threading
from pgu import gui
from Utilities.sorting import *
from Utilities.menu_functions import *
from Classes.Camera import Camera
from Utilities.map_loader import map_loader

FPS = 40
BACKGROUND_COLOR = (0, 0, 0)
WIN_WIDTH = 800
WIN_HEIGHT = 600
DISPLAY = (800, 600)


def hello(message):
    print(message)
    print("Hello!")


# Пока не используется
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                            # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)    # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)                            # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)

screen = pygame.display.set_mode((1000, 700))
screen.fill(pygame.Color(100, 100, 100))

rect_pgu = pygame.Rect(0, 0, 300, 100)

open_dialog = OpenDialog()

data = [
        ('File/Open', open_dialog.open, None),
        ('File/New', None, None),
        ('Edit/Copy', None, None),
        ('Edit/Cut', None, None),
        ('Help/About', None, None),
        ('Help/Reference', None, None),
        ]
menu = gui.Menus(data)
table = gui.Table()
table.td(menu)
table.style.align = -1
table.style.valign = -1

app = gui.App()
app.init(widget=table, screen=screen, area=rect_pgu)


# Загрузка и обработка json-карты
f = open(os.path.join('Maps', 'test_map.json'))

map = json.loads(f.read())

f2 = open(os.path.join('Descriptions', 'objects.json'))
obj_descr = json.loads(f2.read())

objs, back, start_pos = map_loader(map, obj_descr)

f.close()
f2.close()


render_list = objs  # Список словарей с объектами и их функциями (если нет функции - None)
none_render_list = []
clock = pygame.time.Clock()

# camera = Camera(camera_configure, total_level_width, total_level_height)


while True:
    map_address = open_dialog.value
    for e in pygame.event.get():
        app.event(e)
        for obj in render_list:
            obj["object"].event(e)
        for obj in none_render_list:
            obj.event(e)
        if e.type == pygame.QUIT:
            sys.exit()

    if open_dialog.value and open_dialog.value != map_address:
        # Попытка сделать открытие json-карты
        f = open(open_dialog.value)
        map = json.loads(f.read())
        objs, back, start_pos = map_loader(map, obj_descr)
        render_list = objs
        f.close()

    pygame.display.update()

    dt = clock.tick(FPS)
    screen.blit(back, (0, 0))

    for obj in render_list:
        obj["object"].update(dt)

    sort_by_y(render_list)

    for obj in render_list:
        obj["object"].render(screen)

    app.paint()
    pygame.display.flip()
