from Classes.inventory_objs_classes import *


def inventory_objects_parser(names_list):
    inv_objs_list = []
    for o in names_list:
        if o[0] == "Healing Potion":
            inv_objs_list.append(HealingPotion(o[1]))
        if o[0] == "Scarf":
            inv_objs_list.append(Scarf())