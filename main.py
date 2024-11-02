import tkinter as tk
from tkinter import ttk
from classes.DrawGUI import DrawGUI
from classes.Core import Core

class MenuScreen:
    def __init__(self, root, on_search_click):
        self.root = root
        self.frame = tk.Frame(root, bg='#e8f6ff')  # Background màu xanh nhạt
        self.frame.pack(expand=True, fill='both')

        # Create a frame for the group members (left side)
        left_frame = tk.Frame(self.frame, bg='#f0f0f0')
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(20, 10), pady=20)

        # Create a label for "Group Member"
        label = tk.Label(left_frame, text="Group Member", font=("Arial", 24, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        label.pack(anchor='nw', pady=10)

        # List group members
        members = ["22125123 - Lê Khánh Vương", "22125081 - Dương Minh Quang", "21125131 - Huỳnh Hoàng Phúc", "22125081 - Dương Minh Quang"]
        for member in members:
            member_label = tk.Label(left_frame, text=member, font=("Arial", 16), bg='#f0f0f0', fg='#34495e')
            member_label.pack(anchor='nw')

        # Create a frame for buttons (right side)
        right_frame = tk.Frame(self.frame, bg='#e8f6ff')
        right_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 20), pady=20)

        # Create buttons for "Search" and "Quit" with customized styles
        search_button = tk.Button(
            right_frame, text="Search", command=on_search_click, font=("Arial", 24), width=10,
            bg='#3498db', fg='white', activebackground='#2980b9', activeforeground='white', relief='raised', bd=3
        )
        search_button.pack(pady=(0, 10))

        quit_button = tk.Button(
            right_frame, text="Quit", command=self.quit_app, font=("Arial", 24), width=10,
            bg='#e74c3c', fg='white', activebackground='#c0392b', activeforeground='white', relief='raised', bd=3
        )
        quit_button.pack()

        # Configure grid weights for responsive layout
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)
        self.frame.rowconfigure(0, weight=1)

    def show(self):
        self.frame.pack(expand=True, fill='both')

    def hide(self):
        self.frame.pack_forget()

    def quit_app(self):
        self.root.quit()

gui_instance = None

def switch_to_search(root, menu_screen):
    global gui_instance
    
    # Hide the menu screen
    menu_screen.hide()

    if gui_instance is None:
        # Initialize the GUI and core game logic only once
        gui_instance = DrawGUI(root)
        gui_instance.menu_screen = menu_screen  # Thêm tham chiếu đến menu_screen
        core = Core(gui_instance)
    else:
        # Nếu đã tồn tại, chỉ cần hiển thị lại
        gui_instance.main_container.pack(expand=True, fill='both')
   

def main():
    root = tk.Tk()
    root.title("Ares Stone Game")
    root.geometry("1280x720")  # Set consistent size for the window

    # Create the menu screen with a callback to switch to the search screen
    menu_screen = MenuScreen(root, on_search_click=lambda: switch_to_search(root, menu_screen))

    # Show the menu screen initially
    menu_screen.show()

    root.resizable(False, False)  # Prevent window resizing
    root.mainloop()

if __name__ == "__main__":
    main()
