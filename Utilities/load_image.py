from pygame import *
import os

# init()


def load_image(names, path='Pictures', alpha_channel=False):
    # Вызывать после инициации окна pygame
    pictures = []

    if type(names) == list:
        for n in names:
            fullname = os.path.join(path, n)

            try:
                picture = image.load(fullname)  # Загружаем картинку и сохраняем поверхность (Surface)
            except error:  # Если картинки нет на месте
                print("Cannot load image:", n)
                return 0

            if alpha_channel:
                picture.convert_alpha()
            else:
                picture.convert()

            pictures.append(picture)
        return pictures

    else:
        fullname = os.path.join(path, names)
        print(fullname)
        try:
            picture = image.load(fullname)  # Загружаем картинку и сохраняем поверхность (Surface)
        except error:  # Если картинки нет на месте
            print("Cannot load image:", names)
            return 0

        if alpha_channel:
            picture.convert_alpha()
        else:
            picture.convert()

        return picture

if __name__ == '__main__':
    w = 640
    h = 480
    surface = display.set_mode((w, h))
    pic = load_image('1.png')
