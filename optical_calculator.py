"""
Optical Calculator
Basically it is a calculator in which user draws certain numbers and operands like in paint and the program recognizes the pattern using image processing and solves it and displays the output. For image processing, OpenCV and PIL are used(pyscreenshot for Linux).
"""


import tkinter as tk
import tkinter.messagebox as tmb
try:
    from PIL import ImageGrab
except ImportError:
    import pyscreenshot as ImageGrab


class Paint():
    start_x, start_y = 0, 0
    end_x, end_y = 0, 0
    current_item = None
    tool_bar_functions = ("pencil", "eraser", "clear", "calculate")
    selected_tool_bar_function = tool_bar_functions[0]

    def __init__(self, root):
        """
        Constructor for the class and takes the root windows as parameter
        """
        self.root = root
        self.create_menu()
        self.create_tool_bar()
        self.create_drawing_canvas()
        self.bind_mouse()
        self.create_display()
        # following line shows coordinate_label. Use to debug any problems
        # self.create_current_coordinate_label()

    def create_menu(self):
        """
        Create menu bar with file, edit, and aboyt menus
        """
        menu_bar = tk.Menu(self.root)

        # setting up "File" Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New/ Clear", accelerator="Ctrl + N", command=self.clear)
        file_menu.add_command(label="Exit", accelerator="Alt + F4", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # setting up "Tools" Menu
        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Pencil", command=lambda i=0: self.on_tool_bar_button_clicked(i))
        tools_menu.add_command(label="Eraser", command=lambda i=1: self.on_tool_bar_button_clicked(i))
        tools_menu.add_command(label="Clear", accelerator="Ctrl + N", command=lambda i=2: self.on_tool_bar_button_clicked(i))
        tools_menu.add_command(label="Calculate", accelerator="Enter", command=lambda i=3: self.on_tool_bar_button_clicked(i))
        menu_bar.add_cascade(label="Tools", menu=tools_menu)

        # setting up "About" menu
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="About", command=self.display_about_messagebox)
        about_menu.add_command(label="Help", command=self.display_help_messagebox)
        menu_bar.add_cascade(label="About", menu=about_menu)

        self.root.config(menu=menu_bar)

    def display_about_messagebox(self, event=None):
        """
        Display the About messagebox in About menu. Called from within self.create_menu()
        """
        tmb.showinfo("About", "{}\n{}\n{}".format("Optical Calculator\n", "Created By:\nEveryone'n names here\n", "Icons made by Freepik, stephen-hutchings from www.flaticon.com "))

    def display_help_messagebox(self, event=None):
        """
        Display the Help messagebox in About menu. Called from within self.create_menu()
        """
        tmb.showinfo("Help", "1)Draw the calculation using pencil \n2)Press Calculate(equals to sign)\n", icon="question")

    def create_tool_bar(self):
        """
        Create side tool bar with buttons corresponding to the tuple self.tool_bar_functions. (pencil, eraser, clear, calculate)
        """
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack()
        self.tool_bar = tk.Frame(self.top_frame, relief="raised")
        self.tool_bar.pack(fill="y", side="left", pady=3)
        self.create_tool_bar_buttons()
        self.clear_button = tk.Button(self.tool_bar, text="AC", command=self.clear)
        self.button.grid(row=3, sticky="nsew")

    def create_tool_bar_buttons(self):
        """
        Create and grid toolbar buttons, set their icon and connect them to their same named functions , corresponding to the tuple self.tool_bar_functions.
        """
        for i, tool in enumerate(self.tool_bar_functions):
            icon = tk.PhotoImage(file="icons/" + tool + ".gif")
            self.button = tk.Button(self.tool_bar, image=icon, command=lambda i=i: self.on_tool_bar_button_clicked(i))
            self.button.grid(row=i, sticky="nsew")
            self.button.image = icon

    def on_tool_bar_button_clicked(self, index):
        """
        Set self.selected_tool_bar_function to the required function respective to the button clicked,
        and call self.execute_selected_method()
        """
        self.selected_tool_bar_function = self.tool_bar_functions[index]
        self.execute_selected_method()

    def execute_selected_method(self):
        """
        Set the current item we are working on(self.current_item) to None to prevent complications
        and call the respective function corresponding to the button(self.selected_tool_bar_function) by using eval
        """
        self.current_item = None
        self.funcn = eval("self." + self.selected_tool_bar_function)
        self.funcn()

    def pencil(self):
        """
        Function called when user selects pencil from toolbar or tools menu
        Drawing an irregular line while mouse left click-and-drag in tkinter canvas
        """
        self.current_item = self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y)
        self.canvas.bind("<Button1-Motion>", self.pencil_helper)

    def pencil_helper(self, event=None):
        """
        Helper Function for self.pencil() function
        """
        self.start_x, self.start_y = self.end_x, self.end_y
        self.end_x, self.end_y = event.x, event.y
        self.pencil()

    def eraser(self):
        """
        Function called when user selects eraser from toolbar or tools menu
        Removes items under mouse while mouse left click-and-drag in tkinter canvas
        """
        self.canvas.addtag_overlapping("toRemove", self.start_x - 5, self.start_y - 5, self.start_x + 5, self.start_x + 5)
        self.canvas.delete("toRemove")
        self.canvas.bind("<Button1-Motion>", self.eraser_helper)

    def eraser_helper(self, event=None):
        """
        Helper Function for self.eraser() function
        """
        self.start_x, self.start_y = self.end_x, self.end_y
        self.end_x, self.end_y = event.x, event.y
        self.eraser()

    def clear(self, event=None):
        """
        Function called when user selects trashcan from toolbar or tools menu or pressed Ctrl + N
        Clears the tkinter canvas
        """
        self.canvas.delete("all")
        self.selected_tool_bar_function = self.tool_bar_functions[0]

    def calculate(self, event=None):
        """
        Function called when user clicks on "equals" button from toolbar or tool menu or pressed Enter/Return
        Calculates the value of the expression or operation in the canvas
        """
        self.screenshot(self.canvas_frame)
        #processing here
        self.selected_tool_bar_function = self.tool_bar_functions[0]

    def screenshot(self, widget):
        """
        Take screenshot of the canvas(using PIL for windows/mac and pyscreenshot for linux) and saves it in the program directory as "temp.png. Called by self.calculate() "
        """
        x1 = self.root.winfo_rootx() + widget.winfo_x()
        y1 = self.root.winfo_rooty() + widget.winfo_y()
        x2 = x1 + widget.winfo_width()
        y2 = y1 + widget.winfo_height()
        ImageGrab.grab().crop((x1 + 2, y1, x2, y2)).save("temp.png")

    def create_current_coordinate_label(self):
        """
        Create coordinate label(for debugging)
        """
        self.current_coordinate_label = tk.Label(self.tool_bar, text="x: 0\ny: 0", width=5)
        self.current_coordinate_label.grid(row=1000, column=0, padx=2, pady=6, sticky="e")

    def show_current_coordinates(self, event=None):
        """
        Show the coordinate label created by self.create_current_coordinate_label
        """
        x_coordinate, y_coordinate = event.x, event.y
        coordinate_string = "x: {}\ny: {}".format(x_coordinate, y_coordinate)
        self.current_coordinate_label.config(text=coordinate_string)

    def create_drawing_canvas(self):
        """
        Create canvas for drawing the calculations in
        """
        self.canvas_frame = tk.Frame(self.top_frame, width=900, height=900)
        self.canvas_frame.pack(side='right', expand=tk.YES, fill=tk.BOTH)
        self.canvas = tk.Canvas(self.canvas_frame, background="white", width=500, height=300)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def create_display(self):
        """
        Create display for showing answer. Also sets the state of display(text widget) to disabled so the user cannot type there. State of display is only changed when we have to display info.
        """
        self.display = tk.Text(self.root, height=5, state="disabled")
        self.display.pack(side="top", expand="yes", fill="y")

    def bind_mouse(self):
        """
        Bind mouse keys to the functions self.on_mouse_button1_pressed, self.on_mouse_button1_pressed_motion,  self.on_mouse_button1_released, and self.on_mouse_unpressed_motion
        """
        self.canvas.bind("<Button-1>", self.on_mouse_button1_pressed)
        self.canvas.bind("<Button1-Motion>", self.on_mouse_button1_pressed_motion)
        self.canvas.bind("<Button1-ButtonRelease>", self.on_mouse_button1_released)
        self.canvas.bind("<Motion>", self.on_mouse_unpressed_motion)

    def on_mouse_button1_pressed(self, event):
        """
        Set the instance variables according to the event and call self.execute_selected_method()
        Event:When Mouse Left Click
        """
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        (self.end_x, self.end_y) = (self.start_x, self.start_y)
        #print("Start = ", self.start_x, self.start_y)
        self.execute_selected_method()

    def on_mouse_button1_pressed_motion(self, event):
        """
        Set the instance variables according to the event and call self.execute_selected_method()
        Event:When Mouse Left Click and motion
        """
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasx(event.y)
        self.canvas.delete(self.current_item)
        self.execute_selected_method()

    def on_mouse_button1_released(self, event):
        """
        Set the instance variables according to the event and call self.execute_selected_method()
        Event:When Mouse Left Click released
        """
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasx(event.y)
        #print("End = ", self.start_x, self.start_y)

    def on_mouse_unpressed_motion(self, event):
        """
        Set the instance variables according to the event and call self.execute_selected_method()
        Event:When Mouse moved without click
        """
        # following line shows coordinates. use for debugging
        # self.show_current_coordinates(event)
        pass



# Actual Program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Optical Calculator")

    # calling the Paint class constructor
    paint = Paint(root)

    # binding keyboard shortcuts to the window
    root.bind_all("<Control-N>", paint.clear)
    root.bind_all("<Control-n>", paint.clear)
    root.bind_all("<Return>", paint.calculate)
    root.mainloop()
