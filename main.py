import tkinter as tk
import asyncio
from classes.DrawGUI import DrawGUI
from classes.Core import Core

async def update(root):
    while True:
        root.update()
        await asyncio.sleep(1/120)  # ~120 FPS

def main():
    root = tk.Tk()
    root.resizable(True, True)
    root.minsize(1024, 600)

    gui = DrawGUI(root)
    core = Core(gui)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(update(root))
    except tk.TclError:
        # Window was closed
        pass
    finally:
        loop.close()

if __name__ == "__main__":
    main()
