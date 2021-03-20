import tkinter as tk
from tkinter.messagebox import showinfo

import re


class Application:

    # Wrapper class BEGIN

    class WidgetOrCommand:

        def __read_geometry(self):
            gravitation_split = re.compile("/")
            result = gravitation_split.split(self.geometry)

            if len(result) > 1:
                self.gravitation = result[1]
            else:
                self.gravitation = "NEWS"

            rest = result[0]

            row_column_split = re.compile(":")
            row_stuff, column_stuff = row_column_split.split(rest)

            constant_split = re.compile("\+")

            row_stuff = constant_split.split(row_stuff)
            column_stuff = constant_split.split(column_stuff)

            if len(row_stuff) > 1:
                self.height = int(row_stuff[1])
            else:
                self.height = 0

            if len(column_stuff) > 1:
                self.width = int(column_stuff[1])
            else:
                self.width = 0

            rows = row_stuff[0]
            columns = column_stuff[0]

            weight_split = re.compile("\.")

            row_stuff = weight_split.split(rows)
            column_stuff = weight_split.split(columns)

            if len(row_stuff) > 1:
                self.row_weight = int(row_stuff[1])
            else:
                self.row_weight = 1

            if len(column_stuff) > 1:
                self.column_weight = int(column_stuff[1])
            else:
                self.column_weight = 1

            self.row = int(row_stuff[0])
            self.column = int(column_stuff[0])

        def __init__(self, master):
            self.master = master
            pass

        def __call__(self, *args, **kwargs):
            if "text" in kwargs:
                self.category = "widget"
                self.type = args[0]
                self.geometry = args[1]
                self.text = kwargs["text"]

                if "command" in kwargs:
                    self.command = kwargs["command"]

            # probably a command (bind)
            else:
                self.category = "command"
                self.key = args[0]
                self.func = args[1]

        def __getattr__(self, name: str):
            if name not in self.__dict__:
                print("Generating {}".format(name))
                self.__setattr__(name, Application.WidgetOrCommand(master=self))

            return self.__dict__[name]

        def configure_widget(self):
        
            self.__read_geometry()

            self.master.widget.rowconfigure(index=self.row, weight=self.row_weight)
            self.master.widget.columnconfigure(index=self.column, weight=self.column_weight)

            self.widget = self.type(self.master.widget, text=self.text)
            self.widget.grid(column=self.column, row=self.row, sticky=self.gravitation,
                             rowspan=self.height+1, columnspan=self.width+1)

            # Костыль, лень дебажить
            if self.text == "Quit":
                self.widget["command"] = self.widget.quit

            return 0

        def mainloop(self):

            self.configure_widget()

            for child_name in self.__dict__:
                child = self.__dict__[child_name]
                if isinstance(child, Application.WidgetOrCommand):
                    if child != self.master:
                        if child.category == "widget":
                            child.mainloop()

    # Wrapper class END

    def __init__(self, title):

        # Decided not to use title
        self.widget = tk.Tk()

    def mainloop(self):
        self.createWidgets()

        self.configure_window()

        for child_name in self.__dict__:
            child = self.__dict__[child_name]
            if isinstance(child, self.WidgetOrCommand):
                if child.category == "widget":
                    child.mainloop()

        self.widget.mainloop()

    def createWidgets(self):
        pass

    def __getattr__(self, name):
        if name not in self.__dict__:
            print("Generating {}".format(name))
            self.__setattr__(name, self.WidgetOrCommand(master=self))

        return self.__dict__[name]

    def configure_window(self):

        self.widget.rowconfigure(index=1, weight=1)
        self.widget.rowconfigure(index=2, weight=1)
        self.widget.columnconfigure(index=0, weight=1)
        self.widget.columnconfigure(index=1, weight=1)


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))


app = App(title="Sample application")
app.mainloop()



