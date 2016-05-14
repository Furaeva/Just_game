from collections import Counter


class A:
    def __init__(self):
        self.text = 'A'


class B:
    def __init__(self):
        self.text = 'B'


demo_list = [A(), B(), A(), A(), B()]


def group_by_instance(lst):
    objects_text = [el.text for el in lst]
    return Counter(objects_text)

groups = group_by_instance(demo_list)
for group_name in groups.keys():
    print('{} x {}'.format(group_name, groups[group_name]))
