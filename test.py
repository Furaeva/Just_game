from pygame import *
from Utilities.load_image import load_image
import os
import sys
from tkinter import *
from PIL import Image, ImageTk

# init()
#
# screen = display.set_mode((600, 600))
# sur = load_image("chest.gif")
# flo = load_image("flower1.gif")
# screen.blit(sur, (20, 20))
# screen.blit(flo, (300, 70))
#
# while True:
#     for e in event.get():
#         if e.type == QUIT:
#             sys.exit()
#     display.update()
#     display.flip()

root = Tk()
root.geometry("200x200")
# pic = PhotoImage(os.path.join('Pictures', 'flower1.gif'))
pic = PhotoImage(file='Pictures/flower1.gif')
label = Label(root, image=pic)
label.pack()

b = Button(root, justify=LEFT)
photo = Image.open(os.path.join("Pictures", "flower1.gif"))
photo = photo.resize((25, 25), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(photo)
b.config(image=photo, width=25, height=25)
b.pack(side=LEFT)

root.mainloop()