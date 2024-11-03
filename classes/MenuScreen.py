import tkinter as tk
from classes.RoundedButton import RoundedButton
from classes.RoundedButton import RoundedFrame
class MenuScreen:
    def __init__(self, root, on_search_click):
        self.root = root
        self.frame = tk.Frame(root, bg='#d6eaf8')
        self.frame.pack(expand=True, fill='both')

        left_frame = RoundedFrame(self.frame, width=900, height=650, corner_radius=20, bg_color='#f4f6f7', border_color='#154360', border_width=2)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(20, 10), pady=20)


        label = tk.Label(left_frame, text="Group Member", font=("Verdana", 24, 'bold'), bg='#f4f6f7', fg='#154360')
        left_frame.create_window(20, 30, anchor='nw', window=label)

        members = ["22125123 - Lê Khánh Vương", "22125081 - Dương Minh Quang", "21125131 - Huỳnh Hoàng Phúc", "22125080 - Tạ Hoàng Quân"]
        y_offset = 70
        for member in members:
            member_label = tk.Label(left_frame, text=member, font=("Verdana", 16), bg='#f4f6f7', fg='#1f618d')
            left_frame.create_window(20, y_offset, anchor='nw', window=member_label)
            y_offset += 40

        right_frame = tk.Frame(self.frame, bg='#d6eaf8')
        right_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 50), pady=30)

        search_button = RoundedButton(
            right_frame, text="Search", command=on_search_click, bg='#3498db', highlightthickness=0
        )
        search_button.pack(pady=(0, 10), fill='x')  

        quit_button = RoundedButton(
            right_frame, text="Quit", command=self.quit_app, bg='#e74c3c', highlightthickness=0
        )
        quit_button.pack(fill='x')

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)
        self.frame.rowconfigure(0, weight=1)

    def show(self):
        self.frame.pack(expand=True, fill='both')

    def hide(self):
        self.frame.pack_forget()

    def quit_app(self):
        self.root.quit()
