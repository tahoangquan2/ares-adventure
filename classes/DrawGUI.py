import tkinter as tk
from tkinter import ttk

class DrawGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ares Stone Game")
        self.setup_styles()
        self.setup_window()
        self.create_gui_elements()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Sidebar.TFrame', background='#2c3e50')
        style.configure('Game.TFrame', background='#ecf0f1')
        style.configure('Controls.TFrame', background='#ecf0f1')
        style.configure('Modern.TButton', padding=10, font=('Helvetica', 10))
        style.configure('Modern.TLabel', background='#2c3e50', foreground='white', font=('Helvetica', 11))
        style.configure('Controls.TLabel', background='#ecf0f1', font=('Helvetica', 12))

    def setup_window(self):
        self.root.geometry("1280x720")
        self.root.configure(bg='#ecf0f1')
        self.main_container = ttk.Frame(self.root, style='Game.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def create_gui_elements(self):
        self.create_left_sidebar()
        self.create_game_display()
        self.create_right_sidebar()
        self.create_controls()

    def create_left_sidebar(self):
        sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)

        title_label = ttk.Label(sidebar, text="Level Selection", style='Modern.TLabel', font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(20, 10), padx=10)

        list_container = ttk.Frame(sidebar, style='Sidebar.TFrame')
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 20))

        self.input_listbox = tk.Listbox(
            list_container,
            font=('Helvetica', 11),
            bg='#34495e',
            fg='white',
            selectmode=tk.SINGLE,
            relief=tk.FLAT,
            highlightthickness=0,
            selectbackground='#3498db',
            selectforeground='white',
            borderwidth=0
        )

        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.input_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_listbox.config(yscrollcommand=scrollbar.set)

        for i in range(1, 11):
            self.input_listbox.insert(tk.END, f" Level {i:02d}")

    def create_game_display(self):
        game_frame = ttk.Frame(self.main_container, style='Game.TFrame')
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(game_frame,
                              bg='#ffffff',
                              highlightthickness=0,
                              relief=tk.FLAT)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def create_right_sidebar(self):
        sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=250)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        sidebar.pack_propagate(False)

        title_label = ttk.Label(sidebar, text="Algorithm Selection", style='Modern.TLabel', font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(20, 10), padx=10)

        list_container = ttk.Frame(sidebar, style='Sidebar.TFrame')
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 20))

        self.algorithm_listbox = tk.Listbox(
            list_container,
            font=('Helvetica', 11),
            bg='#34495e',
            fg='white',
            selectmode=tk.SINGLE,
            relief=tk.FLAT,
            highlightthickness=0,
            selectbackground='#3498db',
            selectforeground='white',
            borderwidth=0,
            height=2
        )

        algorithms = [" Breadth-First Search", " Depth-First Search"]
        for alg in algorithms:
            self.algorithm_listbox.insert(tk.END, alg)

        self.algorithm_listbox.select_set(0)
        self.algorithm_listbox.pack(fill=tk.BOTH, expand=True)

    def create_controls(self):
        controls = ttk.Frame(self.root, style='Controls.TFrame')
        controls.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        control_container = ttk.Frame(controls, style='Controls.TFrame')
        control_container.pack(anchor='center')

        button_frame = ttk.Frame(control_container, style='Controls.TFrame')
        button_frame.pack()

        self.solve_button = ttk.Button(button_frame,
                                     text="Solve Puzzle",
                                     style='Modern.TButton',
                                     width=15)
        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.play_button = ttk.Button(button_frame,
                                    text="Play",
                                    style='Modern.TButton',
                                    width=15,
                                    state='disabled')
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(button_frame,
                                    text="Next Step",
                                    style='Modern.TButton',
                                    width=15,
                                    state='disabled')
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.weight_var = tk.StringVar(value="Total Weight: 0       Step: 0")
        weight_label = ttk.Label(control_container,
                               textvariable=self.weight_var,
                               font=('Helvetica', 12),
                               style='Controls.TLabel')
        weight_label.pack(pady=(10, 0))

    def draw_state(self, state):
        self.canvas.delete("all")
        if not state.map:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        map_height = len(state.map[0])
        map_width = len(state.map)

        cell_width = canvas_width / (map_width + 2)
        cell_height = canvas_height / (map_height + 2)
        cell_size = min(cell_width, cell_height)

        x_offset = (canvas_width - (map_width * cell_size)) / 2
        y_offset = (canvas_height - (map_height * cell_size)) / 2

        colors = {
            '#': '#34495e',  # Wall
            '$': '#e67e22',  # Stone
            '@': '#e74c3c',  # Ares
            '.': '#f1c40f',  # Switch
            ' ': '#ffffff'   # Empty
        }

        for y in range(map_height):
            for x in range(map_width):
                char = state.map[x][y]
                x1 = x_offset + x * cell_size
                y1 = y_offset + y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                padding = cell_size * 0.2
                x1p, y1p = x1 + padding, y1 + padding
                x2p, y2p = x2 - padding, y2 - padding

                if char == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors['#'], width=0)
                elif char in ['$', '*']:
                    self.canvas.create_oval(x1p, y1p, x2p, y2p, fill=colors['$'], width=0)
                    if char == '*':
                        self.canvas.create_oval(x1p, y1p, x2p, y2p, outline=colors['.'], width=2)
                    weight = state.get_weight(x, y)
                    if weight > 0:
                        text_x = (x1 + x2) / 2
                        text_y = (y1 + y2) / 2
                        self.canvas.create_text(text_x, text_y,
                                             text=str(weight),
                                             fill='white',
                                             font=('Helvetica', int(cell_size / 3)))
                elif char == '@':
                    self.canvas.create_oval(x1p, y1p, x2p, y2p, fill=colors['@'], width=0)
                elif char == '.':
                    self.canvas.create_oval(x1p, y1p, x2p, y2p, fill=colors['.'], width=0)
                elif char == '+':
                    self.canvas.create_oval(x1p, y1p, x2p, y2p,
                                         fill=colors['@'],
                                         outline=colors['.'],
                                         width=3)
