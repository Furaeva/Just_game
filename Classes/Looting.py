import pygame
from Classes.inventory_objs_classes import *


class Looting:
    def __init__(self, visibility):
        self.visibility = visibility
        self.names = []
        self.pos = (0, 0)
        self.sur = pygame.Surface((640, 200), pygame.SRCALPHA)
        if visibility:
            self.sur.fill((100, 100, 100, 70))

    def adds(self, o_list):
        for o in o_list:
            if o.type == 'consume':
                self.names.append('%s x%s' % (o.text, o.number))
            if o.type == 'quest_object':
                self.names.append(o.text)

    def render(self, screen, camera_pos):
        if self.visibility:
            string = ', '.join(self.names)
            string = 'You took: ' + string
            text = Text(string, color=(150, 150, 150), size=24, pos=(20, 20))
            text.render(self.sur)
            self.pos = (self.pos[0] - camera_pos[0], self.pos[1] - camera_pos[1])
            screen.blit(self.sur, self.pos)
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
    loot = Looting(True)
    potion = HealingPotion(5)
    scarf = Scarf()
    loot.adds([potion, scarf])

    while True:
        pygame.display.update()
        screen.fill((0, 0, 0))
        loot.render(screen)
        pygame.display.flip()