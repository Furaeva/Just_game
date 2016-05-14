

class InventoryObject():
    def __init__(self):
        self._text = None

    @property
    def text(self):
        return self._text


class Consume(InventoryObject):
    def __init__(self, number):
        InventoryObject.__init__(self)
        self.number = number

    def render(self):
        pass


class QuestObject(InventoryObject):
    def __init__(self):
        InventoryObject.__init__(self)

    def render(self):
        pass


class HealingPotion(Consume):
    def __init__(self, number):
        Consume.__init__(self, number)
        self.type = 'consume'
        self._text = 'Healing Potion'


class Scarf(QuestObject):
    def __init__(self):
        QuestObject.__init__(self)
        self.type = 'quest_object'
        self._text = 'Scarf'

    def event(self):
        pass
