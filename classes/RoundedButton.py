import tkinter as tk

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, radius=25, bg='#3498db', fg='white', **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.text = text
        self.radius = radius
        self.bg = bg
        self.fg = fg

        # self.configure(width=200, height=60, bg=parent['bg'], highlightthickness=0) 
        # self.button = self.create_rounded_rectangle(5, 5, 195, 55, radius=self.radius, fill=self.bg, outline="")
        # self.text_id = self.create_text(100, 30, text=self.text, font=("Verdana", 15, 'bold'), fill=self.fg)

        self.configure(width=250, height=80, bg=parent['bg'], highlightthickness=0) 

        self.button = self.create_rounded_rectangle(5, 5, 245, 75, radius=self.radius, fill=self.bg, outline="")

        self.text_id = self.create_text(125, 40, text=self.text, font=("Verdana", 18, 'bold'), fill=self.fg)

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2, x1, y2,
            x1, y2-radius, x1, y1+radius, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_enter(self, event):
        self.itemconfig(self.button, fill='#1a73e8')  
        self.itemconfig(self.text_id, fill='#ffffff')  

    def on_leave(self, event):
        self.itemconfig(self.button, fill=self.bg)  
        self.itemconfig(self.text_id, fill=self.fg)  

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius=20, bg_color='#f4f6f7', border_color='#154360', border_width=2, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, **kwargs)
        self.corner_radius = corner_radius

        self.create_rounded_rectangle(0, 0, width, height, corner_radius, fill=bg_color, outline=border_color, width=border_width)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

