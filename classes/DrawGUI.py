import tkinter as tk
from tkinter import ttk

class DrawGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ares Stone Game")

        # Initialize variables before setup
        self.selected_level = tk.StringVar()
        self.selected_algorithm = tk.StringVar()
        self.weight_var = tk.StringVar(value="Total Weight: 0       Step: 0")

        # Create GUI elements
        self.setup_styles()
        self.setup_window()
        self.create_gui_elements()

        # Set default algorithm to BFS
        self.selected_algorithm.set("bfs")
        # Set default level to 1
        self.selected_level.set("1")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Sidebar.TFrame', background='#2c3e50')
        style.configure('Game.TFrame', background='#ecf0f1')
        style.configure('Controls.TFrame', background='#ecf0f1')
        style.configure('Modern.TButton', padding=10, font=('Helvetica', 10))
        style.configure('Modern.TLabel', background='#2c3e50', foreground='white', font=('Helvetica', 11))
        style.configure('Controls.TLabel', background='#ecf0f1', font=('Helvetica', 12))

        # New radio button styles
        style.configure('Sidebar.TRadiobutton',
                       background='#34495e',
                       foreground='white',
                       font=('Helvetica', 11),
                       padding=5)
        style.map('Sidebar.TRadiobutton',
                 background=[('selected', '#3498db'), ('active', '#2980b9')],
                 foreground=[('selected', 'white'), ('active', 'white')])

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

        levels_container = ttk.Frame(sidebar, style='Sidebar.TFrame')
        levels_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 20))

        # Create scrollable frame for levels
        canvas = tk.Canvas(levels_container, bg='#34495e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(levels_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Sidebar.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=220)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add radio buttons for levels
        for i in range(1, 11):
            level_radio = ttk.Radiobutton(
                scrollable_frame,
                text=f"Level {i:02d}",
                value=str(i),
                variable=self.selected_level,
                style='Sidebar.TRadiobutton'
            )
            level_radio.pack(fill=tk.X, pady=2)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas scrolling
        canvas.bind('<Enter>', lambda e: canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units")))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all("<MouseWheel>"))

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

        alg_container = ttk.Frame(sidebar, style='Sidebar.TFrame')
        alg_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 20))

        algorithms = [
            ("Breadth-First Search", "bfs"),
            ("Depth-First Search", "dfs"),
            ("Uniform Cost Search", "ucs"),
            ("A* Search with heuristic", "a_star")
        ]

        for text, value in algorithms:
            alg_radio = ttk.Radiobutton(
                alg_container,
                text=text,
                value=value,
                variable=self.selected_algorithm,
                style='Sidebar.TRadiobutton'
            )
            alg_radio.pack(fill=tk.X, pady=2)

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