import tkinter as tk
from tkinter import messagebox
from tkinter import font
import random

class Application(tk.Frame):
    '''Sample tkinter application class'''

    class Callback:
        def __init__(self, func, button=None):
            self.func = func
            self.button = button
        def __call__(self):
            if self.button != None:
                self.func(self.button)
            else:
                self.func()

    def __init__(self, master=None):
        '''Create root window with frame, tune weight and resize'''
        self.button_list = []
        self.row_num = 4
        self.column_num = 4

        self.session = tk.Tk()
        self.frameConfig(self.session, 2, 1)

        self.frame = tk.Frame(master=self.session)
        self.frame.grid(row=1, column=0, sticky="NSEW")
        self.frameConfig(self.frame, self.row_num, self.column_num)

        self.frameNewExit = tk.Frame(master=self.session)
        self.frameNewExit.grid(row=0, column=0, sticky="NSEW")
        self.frameConfig(self.frameNewExit, 1, 2)
 
        self.createWidgets()

    def frameConfig(self, frame, row_num, column_num):
        
        for i in range(row_num):
            tk.Grid.rowconfigure(frame, i, weight=1)

        for j in range(column_num):
            tk.Grid.columnconfigure(frame, j, weight=1)

    def createButton(self, frame, row_num, column_num, index, text):
        row_pos = index // column_num
        column_pos = index % row_num

        button = tk.Button(frame, text=text, font=tk.font.Font(size = 25), height = 2, width = 6)
        button["command"] = self.Callback(self.exchange, button)
        button.grid(column=column_pos, row=row_pos, sticky="NSEW")

        self.button_list.append(button)

    def createWidgets(self):
        '''Create all the widgets'''
       
        self.button_list = []

        newButton = tk.Button(self.frameNewExit, text="New", height=1, width=8, font=font.Font(size = 25))
        newButton["command"] = self.Callback(self.createWidgets)
        newButton.grid(column=0, row=0, sticky="NSEW")

        
        exitButton = tk.Button(self.frameNewExit, text="Exit", height=1, width=8, font=font.Font(size = 25))
        exitButton["command"] = self.session.quit
        exitButton.grid(column=1, row=0, sticky="NSEW")

        text_list = [""] + list(range(1, 16))
        random.shuffle(text_list)

        for index in range(len(text_list)):
            self.createButton(self.frame, self.row_num, self.column_num, index, str(text_list[index]))

    def exchange(self, button):
        if button["text"] == "":
            return

        button_ind = self.getButtonInd(button)
        neighbouring_empty_ind = self.getEmptyInd(button, self.row_num, self.column_num)
        if neighbouring_empty_ind == None:
            return

        buf = button
        self.button_list[button_ind] = self.button_list[neighbouring_empty_ind]
        self.button_list[neighbouring_empty_ind] = buf
       
        self.renew(self.button_list, self.row_num, self.column_num)
        self.checkWin()

    def renew(self, button_list, row_num, column_num):
        for button_ind, button in enumerate(self.button_list):
            row_pos = button_ind // column_num
            column_pos = button_ind % row_num
            button.grid(column=column_pos, row=row_pos, sticky="NSEW")

    def getButtonInd(self, button):

        for index, value in enumerate(self.button_list):
            if button["text"] == value["text"]:
                return index

    def getEmptyInd(self, button, row_num, column_num):
        button_ind = self.getButtonInd(button)

        row_pos = button_ind // column_num
        column_pos = button_ind % row_num

        if column_pos > 0:
            if self.button_list[button_ind - 1]["text"] == "":
                return button_ind -1
        if column_pos < column_num - 1:
            if self.button_list[button_ind + 1]["text"] == "":
                return button_ind + 1
        if row_pos > 0:
            if self.button_list[button_ind - column_num]["text"] == "":
                return button_ind - column_num
        if row_pos < row_num - 1:
            if self.button_list[button_ind + column_num]["text"] == "":
                return button_ind + column_num

        return None
        
    def checkWin(self):
        length = len(self.button_list)
        for button_ind, button in enumerate(self.button_list):
            if str(button_ind) == button["text"]:
                continue
            else:
                if str(button_ind) == "" and button["text"] == "":
                    continue

            return 

        messagebox.showwarning(title = "win", message = "You win!")
        self.CreateWidgets()


    def launch(self):
        self.session.minsize(self.session.winfo_width(), self.session.winfo_height())
        self.session.mainloop()

app = Application()
app.launch()
