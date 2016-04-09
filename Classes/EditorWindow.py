import tkinter as tk
from pygame import *
import platform
import os
import json
from Utilities.sorting import *
from Utilities.map_loader import *
from Utilities.menu_functions import *

WIDTH = 640
HEIGHT = 480
FPS = 30


class EditorWidow(tk.Frame):
    counter = 0

    def __init__(self, description, open_dialog, *args, **kwargs):
        tk.Frame.__init__(self, *args, width=WIDTH, height=HEIGHT, **kwargs)

        self.description = description
        self.render_list = []

        self.open_dialog = open_dialog

        self.root = args[0]
        self.objs_win = None
        self.walls_win = None

        self.embed = tk.Frame(root, width=640, height=480)
        self.embed.grid(row=0, column=2)
        self.root.update()
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        if platform == 'windows':
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        display.init()
        self.screen = display.set_mode((640, 480))
        display.flip()

        self.show_obj = tk.IntVar()
        self.show_walls = tk.IntVar()
        self.add_menu()

    def add_menu(self):
        menubar = tk.Menu(self.root)
        view_menu = tk.Menu(menubar)
        view_menu.add_checkbutton(label="Objects", onvalue=1, offvalue=0, variable=self.show_obj,
                                  command=self.check_obj_window)
        view_menu.add_checkbutton(label="Walls", onvalue=1, offvalue=0, variable=self.show_walls,
                                  command=self.check_walls_window)
        menubar.add_cascade(label='View', menu=view_menu)
        self.root.config(menu=menubar)

    def check_obj_window(self):
        if self.show_obj.get():
            self.create_objects_window()
        else:
            self.close_window(self.objs_win)

    def check_walls_window(self):
        if self.show_walls.get():
            self.create_walls_window()
        else:
            self.close_window(self.walls_win)

    def check(self):
        print(self.show_obj.get())

    def create_objects_window(self):
        t = tk.Toplevel(self)
        self.objs_win = t
        t.wm_title("Objects Brush")

    def create_walls_window(self):
        t = tk.Toplevel(self)
        self.walls_win = t
        t.wm_title("Walls Brush")

    def close_window(self, win):
        if win:
            win.destroy()

    def m_loop(self, fps=FPS):
        clock = pygame.time.Clock()

        while True:
            map_address = self.open_dialog.file_name

            for e in pygame.event.get():
                for obj in self.render_list:
                    obj["object"].event(e)
                if e.type == pygame.QUIT:
                    sys.exit()

            dt = clock.tick(fps)

            display.update()

            if type(self.back) == dict:
                self.screen.blit(self.back["surface"], (0, 0))
            else:
                self.screen.fill(self.back)

            for obj in self.render_list:
                obj["object"].update(dt)

            sort_by_y(self.render_list)

            for obj in self.render_list:
                obj["object"].render(self.screen)

            display.flip()

            self.root.update()

            if self.open_dialog.file_name and self.open_dialog.file_name != map_address:
                file = open(self.open_dialog.file_name)
                self.map = json.loads(file.read())
                self.render_list, self.back, self.start_pos = map_loader(self.map, self.description)
                file.close()


def on_map_open(file):
    global RUN
    try:
        data = json.load(file)
    except ValueError:
        print("Map data not in JSON, try again")
    else:
        print(data)
    finally:
        file.close()


if __name__ == "__main__":
    f = open(os.path.join("Just_game", "Descriptions", "objects.json"))
    descr = json.loads(f)
    root = tk.Tk()
    open_dialog = OpenDialog(on_map_open)
    main = EditorWidow(descr, open_dialog, root)
    root.mainloop()
