from pygame import *
from settings import IMAGE_PATH
from Utilities.load_image import load_image
from Utilities.inventory_objects_parser import *


class StaticObject(sprite.Sprite):
    def __init__(self, x, y,  picture, height=False):
        sprite.Sprite.__init__(self)
        self.image = load_image(picture, path=IMAGE_PATH, alpha_channel=True)
        if height:
            self.type = "touchable"
            self.rect = Rect(x, y, self.image.get_rect().width, height)
            self.area = Rect((x - 10), (y - 10), (self.image.get_rect().width + 20), (height + 20))
        else:
            self.type = "untouchable"
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            self.area = Rect((x - 10), (y - 10), (self.rect.width + 20), (self.rect.height + 20))

    def update(self, dt, camera_pos):
        self.rect.x -= camera_pos[0]
        self.rect.y -= camera_pos[1]

    def event(self, e):
        pass

    def interaction(self, something):
        pass

    def render(self, screen):
        if self.type == "touchable":
            y = self.rect.y - self.image.get_rect().height + self.rect.height

            # draw.rect(self.image, (120, 120, 120), self.rect)
            screen.blit(self.image, (self.rect.x, y))
            # draw.rect(screen, (100, 100, 100), self.area)
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))


class Chest(StaticObject):
    def __init__(self, names_list, x, y,  picture, height=False):
        StaticObject.__init__(self, x, y,  picture, height)
        self.inventory_objs_list = inventory_objects_parser(names_list)
        print("CHEST:", self.inventory_objs_list)
        self.state = "enabled"

    def to_inventory(self, inv):
        inv += self.inventory_objs_list
        self.inventory_objs_list = []
        self.state = "disabled"

    def interaction(self, inventory):
        if self.state == "enabled":
            self.to_inventory(inventory)
