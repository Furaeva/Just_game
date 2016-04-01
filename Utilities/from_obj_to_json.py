import json
import pygame


def from_obj_to_json(obj_list, back, start_pos):
    json_map = [{"type": "description", "start_player_pos": start_pos},
                {"type": "background", "image": back["image"]}]
    for obj in obj_list:
        obj_dict = {"index": obj["index"], "name": obj["name"], "function": obj["function"]}
        if obj.type == "touchable":
            obj_dict.update({"type": ["object", "touchable"]})
        else:
            obj_dict.update({"type": ["object", "untouchable"]})
    return json_map
