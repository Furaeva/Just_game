from pygame import *
from setting import IMAGE_PATH
from Utilities.load_image import load_image


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

    def update(self, dt):
        pass

    def event(self, e):
        pass

    def interaction(self, something):
        pass

    def render(self, screen):
        if self.type == "touchable":
            y = self.rect.y - self.image.get_rect().height + self.rect.height
            draw.rect(self.image, (120, 120, 120), self.rect)
            screen.blit(self.image, (self.rect.x, y))
            draw.rect(screen, (100, 100, 100), self.area)
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))
