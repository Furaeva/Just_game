import sys
import pygame
from pygame import *
from Classes.inventory_objs_classes import *
from collections import Counter


class Looting:
    def __init__(self):
        self.objects = []
        self.sur = pygame.Surface((640, 200), pygame.SRCALPHA)
        self.sur.fill((100, 100, 100, 70))

    def group_by_instance(self):
        objects_text = [el.text for el in self.objects]
        return Counter(objects_text)

    def adds(self, o_list):
        self.objects += o_list

    def render(self, screen):
        groups = self.group_by_instance()
        dy = 20
        y = 10
        for group_name in groups:
            text = Text('{} x {}'.format(group_name, groups[group_name]), color=(200, 200, 200), size=18,
                        font='Arial')
            surf = text.get_surf()
            self.sur.blit(surf, (0, y))
            y += dy
        # string = ', '.join(self.objects)
        # text = Text(string, color=(150, 150, 150), size=24, pos=(20, 20))
        # text.render(self.sur)
        screen.blit(self.sur, (0, 0))


class Text:
    def __init__(self, text, color=(255, 0, 0), font=None, size=15, pos=(0, 0)):
        self.pos = pos
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(font, size)

    def render(self, surf):
        text_surf = self.font.render(str(self.text), True, self.color)
        surf.blit(text_surf, self.pos)

    def get_surf(self):
        return self.font.render(str(self.text), True, self.color)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode([640, 480])
    loot = Looting()
    for i in range(0, 2):
        potion = HealingPotion(4)
        loot.adds([potion])
        scarf = Scarf()
        loot.adds([scarf])

    while True:
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_ESCAPE or e.type == QUIT:
                sys.exit()
        pygame.display.update()
        screen.fill((0, 0, 0))
        loot.render(screen)
        pygame.display.flip()
