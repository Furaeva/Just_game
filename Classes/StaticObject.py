from pygame import *
from Utilities.load_image import load_image


class StaticObject(sprite.Sprite):
    def __init__(self, x, y,  picture, height=False):
        sprite.Sprite.__init__(self)
        self.image = load_image(picture, alpha_channel=True)
        if height:
            self.type = "touchable"
            self.rect = Rect(x, y, self.image.get_rect().width, height)
            self.area = Rect((x + 10), (y + 10), (self.image.get_rect().width + 10), (height + 10))
        else:
            self.type = "untouchable"
            self.rect = self.image.get_rect()
            self.area = Rect((x + 10), (y + 10), (self.rect.width + 10), (self.rect.height + 10))

    def update(self, dt):
        pass

    def event(self, e):
        pass

    def render(self, screen):
        if self.type == "touchable":
            y = self.rect.y - self.image.get_rect().height + self.rect.height
            screen.blit(self.image, (self.rect.x, y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))
