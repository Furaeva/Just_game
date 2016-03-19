from tkinter import *
import json
from tkinter.filedialog import *


class OpenDialog:
    def __init__(self, cb):
        self.file_name = False
        # Функция, которая будет запущена при открытии файла
        self._cb = cb

    def open(self):
        # root = Tk()
        file = askopenfile()
        self.file_name = file.name
        # file.close()
        # root.destroy()
        self._cb(file)


def stub():
    """
    Функция-заглушка
    """
    pass

