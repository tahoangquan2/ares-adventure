import tkinter as tk
import asyncio
from classes.DrawGUI import DrawGUI
from classes.MenuScreen import MenuScreen
from classes.Core import Core

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ares Stone Game")
        self.root.geometry("1280x720")
        self.root.resizable(True, True)

        # Initialize instance variables
        self.gui_instance = None
        self.core = None
        self.running = True

        # Create menu screen
        self.menu_screen = MenuScreen(self.root, on_search_click=self.switch_to_search)
        self.menu_screen.show()

        # Set up window close handler and bind custom close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<<Close>>", lambda e: self.on_closing())

    def switch_to_search(self):
        # Hide the menu screen
        self.menu_screen.hide()

        if self.gui_instance is None:
            # Initialize the GUI and core game logic for the first time
            self.gui_instance = DrawGUI(self.root)
            self.gui_instance.menu_screen = self.menu_screen
            self.core = Core(self.gui_instance)
        else:
            # Reinitialize GUI and core for subsequent switches
            self.gui_instance = DrawGUI(self.root)
            self.gui_instance.menu_screen = self.menu_screen
            self.core = Core(self.gui_instance)

    def on_closing(self):
        self.running = False
        self.root.destroy()
        # Get the current event loop and stop it
        loop = asyncio.get_event_loop()
        loop.stop()

    async def update(self, interval=1/60):
        while self.running:
            try:
                self.root.update()
                await asyncio.sleep(interval)
            except tk.TclError:
                break
        loop = asyncio.get_event_loop()
        loop.stop()

def main():
    app = App()
    try:
        asyncio.run(app.update())
    except (RuntimeError, KeyboardInterrupt):
        pass
    finally:
        # Ensure the app is properly closed
        if hasattr(app, 'root') and app.root:
            app.root.destroy()

if __name__ == "__main__":
    main()
