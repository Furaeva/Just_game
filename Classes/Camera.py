from pygame import *
from settings import *

#
# class Camera(object):
#     def __init__(self, camera_func, width, height):
#         self.camera_func = camera_func
#         self.state = Rect(0, 0, width, height)
#
#     def apply(self, target):
#         return target.rect.move(self.state.topleft)
#
#     def update(self, target):
#         self.state = self.camera_func(self.state, target.rect)


class Camera:
    def __init__(self, hero, width=640, height=480):
        self.hero = hero
        x = hero.rect.centerx - width / 2
        y = hero.rect.centery - height / 2
        self.rect = Rect(x, y, width, height)
        self.change = (0, 0)

    # def update(self):
    #     x = self.rect.x + self.change[0]
    #     y = self.rect.y + self.change[1]
    #     print(x, y)
    #     self.rect.move_ip(x, y)
