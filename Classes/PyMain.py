from pygame import *
from Utilities.sorting import *
from Utilities.obj_funcs_parser import obj_funcs_parser
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

    def __init__(self, width=640, height=480):
        """Initialize"""
        """Initialize PyGame"""
        init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = display.set_mode((self.width, self.height))
        self.render_list = []
        self.none_render_list = []

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
                    value, objct = hero.area_collision(self.render_list)
                    if value:
                        # Проверка на пересечение с объектами, которым присвоена какая-либо функция
                        obj_funcs_parser(objct)  # Парсинг

                hero.event(e)

                for obj in self.render_list:
                    obj["object"].event(e)
                for obj in self.none_render_list:
                    obj.event(e)
                if e.type == QUIT:
                    sys.exit()

            dt = clock.tick(fps)
            self.screen.fill(BACKGROUND_COLOR)

            for obj in self.render_list:
                obj["object"].update(dt)

            hero.update(dt, self.render_list)

            self.add_render_object({"object": hero, "function": None})  # Добавляем героя в рендер-лист

            sort_by_y(self.render_list)   # Сортируем

            for obj in self.render_list:  # Отрисовываем
                obj["object"].render(self.screen)

            self.del_render_object({"object": hero, "function": None})  # Удаляем героя из рендер-листа

            display.flip()
