import json


def render_list_to_json(render_list, back, start_pos):
    descr = {"type": "description", "start_player_pos": start_pos}
    background = {"type": "background", "image": back}
    future_map = [descr, background]

    for obj_dic in render_list:
        if obj_dic["type"] != "cursor":
            print("render_json ren", obj_dic["name"], obj_dic["class"])
            obj = {"index": obj_dic["index"], "type": obj_dic["type"], "name": obj_dic["name"],
                   "class": obj_dic["class"], "pos": (obj_dic["object"].rect.x, obj_dic["object"].rect.y),
                   "argument": obj_dic["argument"]}
            print("render_json dict", obj["name"], obj["class"])
            future_map.append(obj)

    json_map = json.dumps(future_map, sort_keys=True, indent=4)

    return json_map
