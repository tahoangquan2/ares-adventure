import tkinter as tk
import asyncio
from classes.DrawGUI import DrawGUI
from classes.Core import Core

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(True, True)
        self.root.minsize(1024, 600)

        self.gui = DrawGUI(self.root)
        self.core = Core(self.gui)

        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.running = False
        self.root.quit()
        self.root.destroy()

    async def update(self, interval=1/120):
        while self.running:
            try:
                self.root.update()
                await asyncio.sleep(interval)
            except tk.TclError:
                break

def main():
    app = App()

    try:
        asyncio.run(app.update())
    except RuntimeError:
        pass  # Ignore runtime error on closing

if __name__ == "__main__":
    main()
