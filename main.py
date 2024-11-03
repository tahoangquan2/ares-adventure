import tkinter as tk
from classes.DrawGUI import DrawGUI
from classes.MenuScreen import MenuScreen
from classes.Core import Core

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
        #gui_instance.main_container.pack_forget() 
       # gui_instance.main_container.pack(expand=True, fill='both')
        gui_instance = DrawGUI(root)
        gui_instance.menu_screen = menu_screen 
        core = Core(gui_instance)
        #for widget in gui_instance.main_container.winfo_children():
            #widget.pack_configure()
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
