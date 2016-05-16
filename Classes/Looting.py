import pygame
from Classes.inventory_objs_classes import *


class Looting:
    def __init__(self, visibility, width=640):
        self.visibility = visibility
        self.names = []
        self.sur = pygame.Surface((width, 100), pygame.SRCALPHA)
        if visibility:
            self.sur.fill((0, 0, 0, 70))

    def adds(self, o_list):
        for o in o_list:
            if o.type == 'consume':
                self.names.append('%s x%s' % (o.text, o.number))
            if o.type == 'quest_object':
                self.names.append(o.text)

    def render(self, screen):
        if self.visibility:
            string = ', '.join(self.names)
            string = 'You took: ' + string
            text = Text(string, color=(255, 255, 255), size=24, pos=(20, 20))
            text.render(self.sur)
            screen.blit(self.sur, (0, 0))
        else:
            pass


class Text:
    def __init__(self, text, color=(255, 0, 0), font=None, size=15, pos=(0, 0)):
        self.pos = pos
        self.text = text
        self.color = color
        self.font = pygame.font.Font(font, size)

    def render(self, surf):
        text_surf = self.font.render(str(self.text), True, self.color)
        surf.blit(text_surf, self.pos)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([640, 480])
    loot = Looting()
    for i in range(0, 20):
        potion = Potion()
        loot.adds([potion])

    while True:
        pygame.display.update()
        screen.fill((0, 0, 0))
        loot.render(screen)
        pygame.display.flip()