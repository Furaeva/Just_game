# from tkinter import *
from settings import IMAGE_PATH
from Classes.StaticObject import StaticObject, Chest
from Utilities.load_image import load_image
import json
import os
import pygame


def map_loader(json_map, objects_descr):
    """
    :param json_map: Карта в формате json
    :param objects_descr: Описания предметов в формате json
    :return: Список словарей с объектами и функциями (если есть), бэкграунд
    и стартовую позицию персонажа (кортеж)
    """
    obj_list = []

    for dic in json_map:
        if dic["type"] == "description":
            start_pos = dic["start_player_pos"]

        if dic["type"] == "background":
            # x = y = 0
            # image = dic["image"]
            # back = StaticObject(x, y, image)
            back = {"surface": load_image(dic["image"], path=IMAGE_PATH), "address": dic["image"]}

        if dic["type"] == "object":
            x = dic['pos'][0]
            y = dic['pos'][1]
            for obj in objects_descr[0]["objects"]:
                if dic['name'] == obj['name']:
                    image = obj['image'][0]
                    classname = obj['class']
                    if obj['type'] == 'touchable':
                        height = obj['height']
                    else:
                        height = False

            if classname == "Chest":
                new_obj = Chest(dic["argument"], x, y, image, height=height)
            else:
                new_obj = StaticObject(x, y, image, height=height)
            obj_dict = {"object": new_obj, "argument": dic["argument"], "class": classname,
                        "index": dic["index"], "type": dic["type"], "name": dic["name"]}
            print("map_loader", obj_dict)

            obj_list.append(obj_dict)

    return obj_list, back, start_pos


if __name__ == '__main__':
    s = pygame.display.set_mode((2, 2))
    f = open(os.path.join('Maps', 'test_map.json'))

    map = json.loads(f.read())

    f2 = open(os.path.join('Descriptions', 'objects.json'))
    obj_descr = json.loads(f2.read())

    objs = map_loader(map, obj_descr)

    f.close()
    f2.close()
