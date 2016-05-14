import pygame


class Inventory():
    def __init__(self, hero):
        self.hero = hero
        self.objs = hero.inventory
