# from tkinter import *
from Classes.StaticObject import StaticObject
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
            back = {"surface": load_image(dic["image"]), "address": dic["image"]}

        if dic["type"][0] == "object":
            x = dic['pos'][0]
            y = dic['pos'][1]
            for obj in objects_descr[0]["objects"]:
                if dic['name'] == obj['name']:
                    image = obj['image'][0]
                    if dic['type'][1] == 'touchable':
                        height = obj['height']
                    else:
                        height = False

            new_obj = StaticObject(x, y, image, height=height)
            print(new_obj.rect.x, new_obj.rect.y)
            obj_dict = {"object": new_obj, "function": dic["function"],
                        "index": dic["index"], "type": dic["type"], "name": dic["name"]}

            obj_list.append(obj_dict)

    return obj_list, back, start_pos


def render_list_to_json(render_list, back, start_pos):
    descr = {"type": "description", "start_player_pos": start_pos}
    background = {"type": "background", "image": back}
    future_map = [descr, background]

    for obj_dic in render_list:
        if obj_dic["type"] != "cursor":
            obj = {"index": obj_dic["index"], "type": obj_dic["type"], "name": obj_dic["name"],
                   "pos": (obj_dic["object"].rect.x, obj_dic["object"].rect.y), "function": obj_dic["function"]}
            future_map.append(obj)

            print("!!!!:", obj["pos"])

    json_map = json.dumps(future_map, sort_keys=True, indent=4)

    return json_map


if __name__ == '__main__':
    s = pygame.display.set_mode((2, 2))
    f = open(os.path.join('Maps', 'test_map.json'))

    map = json.loads(f.read())

    f2 = open(os.path.join('Descriptions', 'objects.json'))
    obj_descr = json.loads(f2.read())

    objs = map_loader(map, obj_descr)

    f.close()
    f2.close()
