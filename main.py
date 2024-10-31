import tkinter as tk
from classes.DrawGUI import DrawGUI
from classes.Core import Core

def main():
    root = tk.Tk()

    # Initialize the GUI
    gui = DrawGUI(root)

    # Initialize the core game logic with the GUI
    core = Core(gui)

    root.resizable(True, True)
    root.minsize(1024, 600)

    root.mainloop()

if __name__ == "__main__":
    main()
