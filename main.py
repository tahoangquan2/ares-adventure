import tkinter as tk

from classes.GameUI import GameGUI

if __name__ == "__main__":
	root = tk.Tk()
	app = GameGUI(root)

	root.bind('<Configure>', app.update_display)
	root.resizable(True, True)
	root.minsize(1024, 600)
	root.mainloop()
