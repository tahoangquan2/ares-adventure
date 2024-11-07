import tkinter as tk
from classes.RoundedButton import RoundedButton
from classes.RoundedButton import RoundedFrame

class MenuScreen:
    def __init__(self, root, on_search_click):
        self.root = root
        self.frame = tk.Frame(root, bg='#d6eaf8')
        self.frame.pack(expand=True, fill='both')
        
        # Display game title at the top
        title_label = tk.Label(self.frame, text="Ares Stone Game", font=("Verdana", 32, 'bold'), bg='#d6eaf8', fg='#154360')
        title_label.pack(pady=(30, 10))

        # Create a frame for buttons in vertical alignment
        button_frame = tk.Frame(self.frame, bg='#d6eaf8')
        button_frame.pack(pady=(10, 20))

        # Place buttons vertically
        search_button = RoundedButton(
            button_frame, text="Search", command=on_search_click, bg='#3498db', highlightthickness=0
        )
        search_button.pack(pady=(0, 10), fill='x')

        quit_button = RoundedButton(
            button_frame, text="Quit", command=self.quit_app, bg='#e74c3c', highlightthickness=0
        )
        quit_button.pack(pady=(10, 0), fill='x')

        # Create a frame for the members section to split info evenly on both sides
        members_frame = tk.Frame(self.frame, bg='#d6eaf8')
        members_frame.pack(expand=True, pady=(20, 30))

        # Configure column weights for symmetrical alignment
        members_frame.grid_columnconfigure(0, weight=1)
        members_frame.grid_columnconfigure(1, weight=1)

        # Two evenly-aligned member info sections with adjusted vertical padding
        left_members_frame = RoundedFrame(members_frame, width=400, height=300, corner_radius=20, bg_color='#f4f6f7', border_color='#154360', border_width=2)
        left_members_frame.grid(row=0, column=0, padx=(0, 10), pady=20, sticky="nsew")

        right_members_frame = RoundedFrame(members_frame, width=400, height=300, corner_radius=20, bg_color='#f4f6f7', border_color='#154360', border_width=2)
        right_members_frame.grid(row=0, column=1, padx=(10, 0), pady=20, sticky="nsew")

        # Member info for the left side with extra top padding
        left_members = ["22125123 - Lê Khánh Vương", "22125081 - Dương Minh Quang"]
        y_offset = 60  # Increased top padding for better vertical centering
        for member in left_members:
            member_label = tk.Label(left_members_frame, text=member, font=("Verdana", 16), bg='#f4f6f7', fg='#1f618d')
            left_members_frame.create_window(20, y_offset, anchor='nw', window=member_label)
            y_offset += 40

        # Member info for the right side with extra top padding
        right_members = ["21125131 - Huỳnh Hoàng Phúc", "22125080 - Tạ Hoàng Quân"]
        y_offset = 60  # Increased top padding for better vertical centering
        for member in right_members:
            member_label = tk.Label(right_members_frame, text=member, font=("Verdana", 16), bg='#f4f6f7', fg='#1f618d')
            right_members_frame.create_window(20, y_offset, anchor='nw', window=member_label)
            y_offset += 40

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

    def show(self):
        self.frame.pack(expand=True, fill='both')

    def hide(self):
        self.frame.pack_forget()

    def quit_app(self):
        self.root.quit()
