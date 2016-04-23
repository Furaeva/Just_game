import sys
import pygame
from Classes.PyMain import PyMain
# from pygame import *

from Utilities.load_image import load_image
from Utilities.map_loader import object_converter


class SuperPyMain(PyMain):
    def mainloop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                for obj in self.render_list:
                    obj.event(event)
                for obj in self.none_render_list:
                    obj.event(event)
                if event.type == pygame.QUIT:
                    sys.exit()
            dt = clock.tick(40)
            self.screen.fill((0, 0, 0))
            for render_obj in self.render_list:
                render_obj.render(self.screen)
                render_obj.update(dt)

            pygame.display.flip()


class DemoCursor:
    def __init__(self, obj_dict, render_list):
        self.obj_dict = obj_dict
        self.render_list = render_list

        if obj_dict:
            self.image = obj_dict["object"].image
            self.rect = obj_dict["object"].rect
        else:
            self.rect = pygame.Rect(10, 10, 0, 0)

    def event(self, event):
        if self.obj_dict:
            if event.type == pygame.MOUSEMOTION:
                print(event.pos)
                self.rect.center = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.obj_dict["object"].rect = self.rect
                self.render_list.append(self.obj_dict)
                self.obj_dict = False

    def update(self, pos):
        # self.rect.move(*pos)
        pass

    def render(self, screen):
        if self.obj_dict:
            screen.blit(self.image, self.rect)
        else:
            pass


if __name__ == "__main__":
    window = SuperPyMain()
    obj = DemoCursor("locker.png")
    window.add_render_object(obj)
    window.mainloop()
