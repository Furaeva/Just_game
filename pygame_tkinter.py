from tkinter import *
from tkinter.filedialog import *
import platform
import pygame
import json
import os
from Utilities.map_loader import map_loader
from Utilities.sorting import *
from Utilities.menu_functions import *

FPS = 40


def on_map_open(file):
    global RUN
    try:
        data = json.load(file)
        render_list, back, start_pos = map_loader(data, obj_descr)
    except ValueError:
        print("Map data not in JSON, try again")
    else:
        print(data)
    finally:
        file.close()


root = Tk()
embed = Frame(root, width=640, height=480)
embed.grid(row=0, column=2)
# playpausebutton = Button(root, command=playpause, text="Play/Pause")
# playpausebutton.grid(row=1, column=2)
root.update()
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
if platform == 'windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'

pygame.display.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.flip()


f2 = open(os.path.join('Descriptions', 'objects.json'))
obj_descr = json.loads(f2.read())

# create file_dialod
open_dialog = OpenDialog(on_map_open)

# add menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=open_dialog.open)
filemenu.add_command(label="Save", command=open_dialog.open)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=stub)
editmenu.add_command(label="Copy", command=stub)
editmenu.add_command(label="Paste", command=stub)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=stub)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)
RUN = True

clock = pygame.time.Clock()
render_list = []
none_render_list = []
start_pos = (0, 0)
back = (100, 100, 100)

while RUN:
    map_address = open_dialog.file_name

    for e in pygame.event.get():
        for obj in render_list:
            obj["object"].event(e)
        for obj in none_render_list:
            obj.event(e)
        if e.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()

    dt = clock.tick(FPS)

    if type(back) == dict:
        screen.blit(back["surface"], (0, 0))
    else:
        screen.fill(back)

    for obj in render_list:
        obj["object"].update(dt)

    sort_by_y(render_list)

    for obj in render_list:
        obj["object"].render(screen)

    pygame.display.flip()
    root.update()

    if open_dialog.file_name and open_dialog.file_name != map_address:
        f = open(open_dialog.file_name)
        map = json.loads(f.read())
        objs, back, start_pos = map_loader(map, obj_descr)
        render_list = objs
        print(render_list)
        f.close()
