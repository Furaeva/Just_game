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
        self.start_camera_pos = Rect(self.start_pos[0] - self.width/2, self.start_pos[1] - self.height/2,
                                     self.width, self.height)
        self.camera_pos = self.start_camera_pos
        self.camera_change = (0, 0)
        self.none_render_list = []
        self.looting = Looting(False)
        self.pos_all()

    def pos_all(self):
        self.back["pos"] = (self.back["pos"][0] - self.start_camera_pos.x,
                            self.back["pos"][1] - self.start_camera_pos.y)
        for o in self.render_list:
            o["object"].rect.x -= self.start_camera_pos.x
            o["object"].rect.y -= self.start_camera_pos.y
        self.looting.pos = (self.looting.pos[0] - self.start_camera_pos.x,
                            self.looting.pos[1] - self.start_camera_pos.y)

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
        while True:
            for e in event.get():
                if e.type == KEYDOWN and e.key == K_SPACE:
                    self.looting = Looting(False)
                    # Проверка на пересечение с объектами, которым присвоена какая-либо функция
                    value, objct = hero.area_collision(self.render_list)
                    if value:
                        if objct["name"] == "chest" and objct["object"].state == 'enabled':
                            self.looting = Looting(True)
                            self.looting.pos = self.camera_pos
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
            self.camera_change = hero.update(dt, self.render_list)
            print("CAM CHANGE", self.camera_change)

            self.back["pos"] = (self.back["pos"][0] - self.camera_change[0],
                                self.back["pos"][1] - self.camera_change[1])
            self.screen.blit(self.back["surface"], self.back["pos"])

            for obj in self.render_list:
                obj["object"].update(dt, self.camera_change)

            self.add_render_object({"object": hero})  # Добавляем героя в рендер-лист

            sort_by_y(self.render_list)   # Сортируем

            for obj in self.render_list:  # Отрисовываем
                obj["object"].render(self.screen)

            self.del_render_object({"object": hero})  # Удаляем героя из рендер-листа

            self.looting.render(self.screen, self.camera_change)
            self.camera_pos = (self.camera_pos[0] - self.camera_change[0],
                               self.camera_pos[1] - self.camera_change[1])

            display.flip()
