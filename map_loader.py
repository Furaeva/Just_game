# from tkinter import *
from Classes.StaticObject import StaticObject
import json
import os


def map_loader(json_map, objects_descr):
    """
    :param json_map: Карта в формате json
    :param objects_descr: Описания предметов в формате json
    :return: Список объектов, который идёт на рендер
    """
    obj_list = []
    for dic in json_map:
        x = dic['pos'][0]
        y = dic['pos'][1]
        for obj in objects_descr:
            if dic['name'] == obj['name']:
                picture = obj['image']
                if dic['type'] == 'object':
                    height = obj['height']
                else:
                    height = False

        new_obj = StaticObject(x, y, picture, height=height)
        print(new_obj.image)

        obj_list.append(new_obj)


f = open(os.path.join('Maps', 'test_map.json'))

map = json.loads(f.read())

f2 = open(os.path.join('Descriptions', 'objects.json'))
obj_descr = json.loads(f2.read())

map_loader(map, obj_descr)

f.close()
f2.close()
