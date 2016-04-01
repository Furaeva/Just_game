import tkinter as tk


class MainWindow(tk.Frame):
    counter = 0

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, width=200, height=100, **kwargs)
        self.button = tk.Button(self, text="Check", command=self.check)
        # self.button_close = tk.Button(self, text="Close window", command=self.close_window)
        # self.button.pack(side="top")
        self.button.pack(side="top")
        self.root = args[0]
        self.children_window = None

        self.show_brush = tk.IntVar()
        self.add_menu()

    def add_menu(self):
        menubar = tk.Menu(self.root)
        view_menu = tk.Menu(menubar)
        view_menu.add_checkbutton(label="Show Brush", onvalue=1, offvalue=0, variable=self.show_brush,
                                  command=self.check_window)
        menubar.add_cascade(label='View', menu=view_menu)
        self.root.config(menu=menubar)

    def check_window(self):
        if self.show_brush.get():
            self.create_window()
        else:
            self.close_window()

    def check(self):
        print(self.show_brush.get())

    def create_window(self):
        self.counter += 1
        t = tk.Toplevel(self)
        self.children_windows = t
        t.wm_title("Window #%s" % self.counter)
        l = tk.Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def close_window(self):
        if self.children_windows:
            self.children_windows.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()