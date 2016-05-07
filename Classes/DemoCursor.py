import sys
import pygame
from settings import IMAGE_PATH
from Classes.PyMain import PyMain
from Utilities.load_image import load_image
from Classes.StaticObject import StaticObject


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
    def __init__(self, description, render_list):
        self.description = description
        self.render_list = render_list

        if description:
            self.obj_list = {}
            self.index = len(self.render_list) + 1
            self.image = load_image(description["image"][0], path=IMAGE_PATH)
            self.pos_rect = self.image.get_rect()
            self.rect = pygame.Rect((self.image.get_rect().x, self.image.get_rect().y),
                                    (self.image.get_rect().width, description["height"]))

            self.a = self.pos_rect.center[1] - self.rect.center[1]
        else:
            self.rect = pygame.Rect(10, 10, 0, 0)
            self.pos_rect = self.rect

    def event(self, event):
        if self.description:
            if event.type == pygame.MOUSEMOTION:
                self.pos_rect.center = event.pos
                self.rect.center = (event.pos[0], event.pos[1] + self.a)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.description["type"] != "untouchable":
                    new_obj = StaticObject(self.rect.x, self.rect.y, self.description["image"][0],
                                           height=self.description["height"])
                    self.obj_list = {"object": new_obj, "argument": None,
                                     "type": "object", "index": self.index,
                                     "name": self.description["name"]}
                else:
                    new_obj = StaticObject(self.pos_rect.x, self.pos_rect.y, self.description["image"][0])
                    self.obj_list = {"object": new_obj, "argument": None,
                                     "type": "object", "index": self.index,
                                     "name": self.description["name"]}

                self.render_list.append(self.obj_list)
                self.description = False

    def update(self, pos):
        # self.rect.move(*pos)
        pass

    def render(self, screen):
        if self.description:
            screen.blit(self.image, self.pos_rect)
        else:
            pass


if __name__ == "__main__":
    window = SuperPyMain()
    obj = DemoCursor("locker.png")
    window.add_render_object(obj)
    window.mainloop()
