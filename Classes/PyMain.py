from pygame import *
from Utilities.sorting import *
from Utilities.map_loader import map_loader
from Classes.Looting import Looting
from Classes.Camera import Camera

import sys

FPS = 30
BACKGROUND_COLOR = (0, 0, 0)
left = right = up = down = False


class PyMain:
    """
    The Main PyMan Class - This class handles the main
    initialization and creating of the Game.
    v.0.2 (edit:20.05.2014)
    """

    def __init__(self, json_map, description,  width=640, height=480):
        """Initialize"""
        """Initialize PyGame"""
        init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = display.set_mode((self.width, self.height))
        self.render_list, self.back, self.start_pos = map_loader(json_map, description)
        self.camera = None
        self.none_render_list = []
        self.looting = Looting(False)

    def add_render_object(self, obj):
        self.render_list.append(obj)

    def add_none_render_object(self, obj):
        self.none_render_list.append(obj)

    def del_render_object(self, obj):
        self.render_list.remove(obj)

    def addEventListener(self, obj, event_type):
        raise "Change me"

    def mainloop(self, hero, fps=FPS):
        """This is the Main Loop of the Game"""
        clock = time.Clock()
        self.camera = Camera(hero, width=self.width, height=self.height)
        while True:
            for e in event.get():
                if e.type == KEYDOWN and e.key == K_SPACE:
                    self.looting = Looting(False)
                    # Проверка на пересечение с объектами, которым присвоена какая-либо функция
                    value, objct = hero.area_collision(self.render_list)
                    if value:
                        if objct["name"] == "chest" and objct["object"].state == 'enabled':
                            self.looting = Looting(True)
                            self.looting.adds(objct["object"].inventory_objs_list)
                            objct["object"].interaction(hero.inventory)
                            objct["argument"] = []
                            print("INVENTORY:", hero.inventory)
                        else:
                            objct["object"].interaction(objct["argument"])

                hero.event(e)

                for obj in self.render_list:
                    obj["object"].event(e)
                for obj in self.none_render_list:
                    obj.event(e)
                if e.type == QUIT:
                    sys.exit()

            dt = clock.tick(fps)

            for obj in self.render_list:
                obj["object"].update(dt, self.camera.change)

            self.back["pos"] = (self.back["pos"][0] + self.camera.change[0],
                                self.back["pos"][1] + self.camera.change[1])

            self.camera.change = hero.update(dt, self.render_list, self.camera.change)

            self.add_render_object({"object": hero})  # Добавляем героя в рендер-лист

            sort_by_y(self.render_list)   # Сортируем

            self.screen.blit(self.back["surface"], self.back["pos"])

            for obj in self.render_list:  # Отрисовываем
                obj["object"].render(self.screen)

            self.del_render_object({"object": hero})  # Удаляем героя из рендер-листа

            self.looting.render(self.screen)

            display.flip()
