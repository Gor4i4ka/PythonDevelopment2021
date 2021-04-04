import tkinter as tk
from tkinter.messagebox import showinfo

import re


class Application:

    possible_figure_colour_list = ["red", "green"]
    current_canvas_object_id = None
    current_canvas_object_x_start = None
    current_canvas_object_y_start = None
    current_canvas_object_creation_stage = False

    def __init__(self, title):

        # Window creation

        self.window = tk.Tk()
        self.window.title = title
        self.window.rowconfigure(index=0, weight=10)
        self.window.rowconfigure(index=1, weight=1)
        self.window.columnconfigure(index=0, weight=1)
        self.window.columnconfigure(index=1, weight=1)
        self.window.grid()

        # Text creation

        self.text_editor = tk.Text(master=self.window)
        self.text_editor.grid(column=0, row=0, sticky="NESW")

        # Canvas creation

        self.canvas = tk.Canvas(master=self.window)
        self.canvas.grid(column=1, row=0, sticky="NESW")
        self.canvas.bind("<Button-1>", self.canvas_create_or_move_oval)
        self.canvas.bind("<B1-Motion>", self.canvas_adjust_or_move_oval)

        # Buttons creation

        self.render_button = tk.Button(master=self.window, text="Render by text", command=self.render_by_text)
        self.render_button.grid(row=1, column=0, sticky="NESW")
        self.write_button = tk.Button(master=self.window, text="Write text by figures", command=self.write_text_by_figures)
        self.write_button.grid(row=1, column=1, sticky="NESW")

    # Create figures by text

    def parse_single_tag(self, tag_string: str, tag_num: int):

        # 0 - x1
        # 1 - y1
        # 2 - x2
        # 3 - y2
        # 4 - colour

        re_expression = re.compile("/")
        split_result = re_expression.split(tag_string)

        if len(split_result) == 5:
            try:
                x1 = int(split_result[0])
                y1 = int(split_result[1])
                x2 = int(split_result[2])
                y2 = int(split_result[3])
                colour = split_result[4]
                if colour not in self.possible_figure_colour_list:
                    return None
                return x1, y1, x2, y2, colour
            except ValueError:
                return None

        return None

    def find_all_tags(self, text_string: str):

        search_pattern = re.compile("\([^\(|^\)]*\)")

        str_end = len(text_string)
        cur_pos = 0

        # 0 - tag_name
        # 1 - [] - start and end

        tag_array = []

        while cur_pos < str_end:
            search_result = search_pattern.search(text_string, pos=cur_pos)
            if search_result:
                tag_span = search_result.span()
                tag_array.append([text_string[tag_span[0] + 1:tag_span[1] - 1], [tag_span[0], tag_span[1]]])

            else:
                break

            cur_pos = tag_span[1]

        return tag_array

    def render_oval_by_tag(self, parsed_tag):
        self.current_canvas_object_id = self.canvas.create_oval(parsed_tag[0], parsed_tag[1], parsed_tag[2], parsed_tag[3], fill=parsed_tag[4])
        self.canvas.itemconfigure(self.current_canvas_object_id, tag=str(self.current_canvas_object_id))

    def create_positive_tag(self, tag):
        self.text_editor.tag_add(tag[0], "1.0 + " + str(tag[1][0]) + " chars", "1.0 + " + str(tag[1][1]) + " chars")
        self.text_editor.tag_config(tag[0], background="green")

    def create_negative_tag(self,tag):
        self.text_editor.tag_add(tag[0], "1.0 + " + str(tag[1][0]) + " chars", "1.0 + " + str(tag[1][1]) + " chars")
        self.text_editor.tag_config(tag[0], background="red")

    def render_by_text(self):

        # Clearing Canvas
        self.canvas.delete("all")

        text_input = self.text_editor.get("1.0", tk.END)
        tag_list = self.find_all_tags(text_input)
        tag_num = 0

        for tag in tag_list:
            parsed_tag = self.parse_single_tag(tag[0], tag_num)
            tag_num += 1

            if parsed_tag:
                self.render_oval_by_tag(parsed_tag)
                self.create_positive_tag(tag)
            else:
                self.create_negative_tag(tag)

        return

    # Create text by figures

    def write_text_by_figures(self):

        self.text_editor.delete("1.0", tk.END)
        current_pos = 0

        object_list = self.canvas.find_all()

        for object_id in object_list:
            x1, y1, x2, y2 = self.canvas.coords(object_id)
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            colour = self.canvas.itemcget(object_id, "fill")

            object_info = "(" + str(x1) + "/" + str(y1) + "/" + str(x2) + "/" + str(y2) + "/" + colour + ")\n"
            self.text_editor.insert("1.0 + " + str(current_pos) + " chars", object_info)
            current_pos += len(object_info)

        return

    def canvas_adjust_or_move_oval(self, event):

        if self.current_canvas_object_id and self.current_canvas_object_creation_stage:

            x2 = event.x
            y2 = event.y
            self.canvas.coords(self.current_canvas_object_id,
                                min(self.current_canvas_object_x_start, x2),
                                min(self.current_canvas_object_y_start, y2),
                                max(self.current_canvas_object_x_start, x2),
                                max(self.current_canvas_object_y_start, y2))

        if self.current_canvas_object_id and not self.current_canvas_object_creation_stage:
            x1, y1, x2, y2 = self.canvas.coords(self.current_canvas_object_id)

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            x_mid = (x1 + x2) / 2
            y_mid = (y1 + y2) / 2

            x_mid_new = event.x
            y_mid_new = event.y

            x_d = x_mid_new - x_mid
            y_d = y_mid_new - y_mid

            self.canvas.coords(self.current_canvas_object_id, x1 + x_d, y1 + y_d, x2 + x_d, y2 + y_d)

    def canvas_create_or_move_oval(self, event):

        x1 = event.x
        y1 = event.y

        if not self.canvas.find_overlapping(x1, y1, x1, y1):
            self.current_canvas_object_creation_stage = True
            self.current_canvas_object_x_start = x1
            self.current_canvas_object_y_start = y1
            self.current_canvas_object_id = self.canvas.create_oval(x1, y1, x1, y1, fill="red")
            self.canvas.itemconfigure(self.current_canvas_object_id, tag=str(self.current_canvas_object_id))
        else:
            self.current_canvas_object_creation_stage = False
            self.current_canvas_object_id = self.canvas.find_closest(x1, y1)

    def mainloop(self):
        self.window.geometry("1200x800+300+0")
        self.window.mainloop()

app = Application(title="Sample application")
app.mainloop()