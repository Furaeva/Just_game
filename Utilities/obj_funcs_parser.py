from Utilities.object_functions import *


def obj_funcs_parser(obj):
    if obj["function"][0] == "Hello":
        hello(obj["function"][1])