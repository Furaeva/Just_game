import tkinter as tk
import pygame
from pygame import *
import PIL as pil
from PIL import Image, ImageTk
import platform
import os
from Utilities.sorting import *
from Utilities.map_loader import *
from Utilities.render_list_to_json import *
from Utilities.menu_functions import *
from Classes.DemoCursor import DemoCursor


WIDTH = 640
HEIGHT = 480
FPS = 30


class EditorWidow(tk.Frame):
    counter = 0

    def __init__(self, description, open_dialog, *args, **kwargs):
        tk.Frame.__init__(self, *args, width=WIDTH, height=HEIGHT, **kwargs)

        self.description = description
        self.render_list = []
        self.objects_list = []
        self.walls_list = []
        self.back = (100, 100, 100)
        self.start_pos = None
        self.cursor = DemoCursor(False, False)

        self.open_dialog = open_dialog

        self.root = args[0]
        self.root.geometry("+100+100")
        self.objs_win = None
        self.walls_win = None

        self.embed = tk.Frame(root, width=640, height=480)
        self.embed.grid(row=0, column=2)
        self.root.update()
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        if platform == 'windows':
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        # pygame.display.flip()

        self.show_obj = tk.IntVar()
        self.show_walls = tk.IntVar()
        self.add_menu()
        self.root.bind('<Motion>', self.on_mouse_move)
        self.root.bind('<Button-1>', self.on_mouse_button)

    def on_mouse_button(self, event):
        e = pygame.event.Event(MOUSEBUTTONDOWN, {"pos": (event.x, event.y), "button": 1})
        pygame.event.post(e)

    def on_mouse_move(self, event):
        e = pygame.event.Event(MOUSEMOTION, {"pos": (event.x, event.y)})
        pygame.event.post(e)

    def add_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_dialog.open)
        filemenu.add_command(label="Save", command=self.save_map)
        filemenu.add_command(label="Close", command=self.open_dialog.close)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        view_menu = tk.Menu(menubar)
        view_menu.add_checkbutton(label="Objects", onvalue=1, offvalue=0, variable=self.show_obj,
                                  command=self.check_obj_window)
        view_menu.add_checkbutton(label="Walls", onvalue=1, offvalue=0, variable=self.show_walls,
                                  command=self.check_walls_window)
        menubar.add_cascade(label='View', menu=view_menu)
        edit_menu = tk.Menu(menubar)
        edit_menu.add_command(label="Clean", command=self.clean)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        self.root.config(menu=menubar)

    def save_map(self):
        json_map = render_list_to_json(self.render_list, self.back["address"], self.start_pos)
        file = open(self.open_dialog.file_name, "w")
        file.writelines(json_map)
        file.close()

    def clean(self):
        self.render_list = []
        self.cursor = DemoCursor(False, False)

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

    def create_objects_window(self):
        t = tk.Toplevel(self)
        self.objs_win = t
        t.wm_title("Objects Brush")
        t.geometry("+800+400")
        t.resizable(width=False, height=False)
        t.transient(self.root)

        canvas = tk.Canvas(t, width=200, height=200)
        frame = tk.Frame(canvas, width=200, height=200)
        vsb = tk.Scrollbar(t, orient="vertical")
        canvas.configure(yscrollcommand=vsb.set)

        frame.pack(side=LEFT)
        vsb.pack(side="right", fill='y')
        canvas.pack(side="right", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        brushes = []

        for obj in self.description[0]["objects"]:
            self.create_brush(frame, obj, brushes)

        vsb.configure(command=canvas.yview)

        frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    def create_walls_window(self):
        t = tk.Toplevel(self)
        self.walls_win = t
        t.wm_title("Walls Brush")
        t.geometry("+800+100")
        t.transient(self.root)

    def create_brush(self, frame, obj, brushes):
        b = tk.Button(frame)

        photo = pil.Image.open(os.path.join("..", "Pictures", obj["icon"]))
        photo = photo.resize((25, 25), pil.Image.ANTIALIAS)
        photo = pil.ImageTk.PhotoImage(photo)

        b.config(image=photo, width=25, height=25, command=lambda: self.get_object(obj["index"]))
        b.image = photo

        b.grid(row=len(brushes)//6, column=len(brushes) % 6 + 1)

        brushes.append(b)

    def get_object(self, index):
        for obj in self.description[0]["objects"]:
            if obj["index"] == index:
                self.cursor = DemoCursor(obj, self.render_list)

    def close_window(self, win):
        if win:
            win.destroy()

    def m_loop(self, fps=FPS):
        clock = pygame.time.Clock()

        while True:
            map_address = self.open_dialog.file_name

            for e in pygame.event.get():
                self.cursor.event(e)

                if self.cursor.render_list:
                    self.render_list = self.cursor.render_list

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

            self.render_list.append({"object": self.cursor, "type": "cursor"})

            sort_by_y(self.render_list)

            for obj in self.render_list:
                obj["object"].render(self.screen)

            self.render_list.remove({"object": self.cursor, "type": "cursor"})

            display.flip()

            self.root.update()

            if self.open_dialog.file_name and self.open_dialog.file_name != map_address:
                file = open(self.open_dialog.file_name)
                json_map = json.loads(file.read())
                self.render_list, self.back, self.start_pos = map_loader(json_map, self.description)
                file.close()
            if not self.open_dialog.file_name:
                self.render_list = []
                self.cursor = DemoCursor(False, False)
                self.back = (100, 100, 100)


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
    f = open(os.path.join("..", "Descriptions", "objects.json"))
    descr = json.load(f)
    root = tk.Tk()
    open_dialog = OpenDialog(on_map_open)
    main = EditorWidow(descr, open_dialog, root)
    f.close()
    main.m_loop()
