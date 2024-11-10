import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class DrawGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ares Stone Game")

        # Initialize variables
        self.selected_level = tk.StringVar()
        self.selected_algorithm = tk.StringVar()
        self.weight_var = tk.StringVar(value="Total Weight: 0       Step: 0")

        # Load images
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.wall_image = Image.open(os.path.join(current_dir, "graphics/kenney_sokobanPack/PNG/Retina/Blocks/block_01.png"))
            self.stone_image = Image.open(os.path.join(current_dir, "graphics/kenney_sokobanPack/PNG/Retina/Stone/tile000.png"))
            self.ares_image = Image.open(os.path.join(current_dir, "graphics/kenney_sokobanPack/PNG/Retina/Player/player_03.png"))
            self.switch_image = Image.open(os.path.join(current_dir, "graphics/kenney_sokobanPack/PNG/Retina/Environment/environment_10.png"))
            self.empty_image = Image.open(os.path.join(current_dir, "graphics/kenney_sokobanPack/PNG/Retina/Ground/ground_04.png"))
            self.surround_image = Image.open(os.path.join(current_dir, "graphics/kenney_sokobanPack/PNG/Retina/Environment/environment_06.png"))
        except Exception as e:
            raise

        # Create GUI elements
        self.setup_styles()
        self.setup_window()
        self.create_gui_elements()

        # Set defaults
        self.selected_algorithm.set("bfs")
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

        canvas = tk.Canvas(levels_container, bg='#34495e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(levels_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Sidebar.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=220)
        canvas.configure(yscrollcommand=scrollbar.set)

        for i in range(1, 13):
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

        self.back_button = ttk.Button(button_frame,
                                    text="Back",
                                    style='Modern.TButton',
                                    command=self.on_back_pressed,
                                    width=15)
        self.back_button.pack(side=tk.LEFT, padx=5)

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

        self.reset_button = ttk.Button(button_frame,
                                    text="Reset",
                                    style='Modern.TButton',
                                    width=15)
        self.reset_button.pack_forget()

        weight_label = ttk.Label(control_container,
                                textvariable=self.weight_var,
                                font=('Helvetica', 12),
                                style='Controls.TLabel')
        weight_label.pack(pady=(10, 0))

    def on_back_pressed(self):
        if hasattr(self.root, 'core') and self.root.core:
            self.root.core.reset_full_state()

        # Clear existing canvas
        self.canvas.delete("all")

        # Reset UI components
        self.selected_level.set("1")
        self.selected_algorithm.set("bfs")
        self.weight_var.set("Total Weight: 0       Step: 0")

        # Show solve button and hide play/next buttons
        self.solve_button.pack(side=tk.LEFT, padx=5)
        self.solve_button.config(text="Solve Puzzle", state='normal')
        self.play_button.pack_forget()
        self.next_button.pack_forget()

        # Clean up the main container
        for widget in self.main_container.winfo_children():
            widget.pack_forget()

        self.main_container.pack_forget()
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame) and (not hasattr(widget, 'frame') or widget != self.menu_screen.frame):
                widget.pack_forget()

        # Show menu screen
        if hasattr(self, 'menu_screen'):
            self.menu_screen.show()

    def draw_state(self, state):
        self.canvas.delete("all")

        # Validate state
        if not hasattr(state, 'width') or not hasattr(state, 'height'):
            return

        if state.width == 0 or state.height == 0:
            return

        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # If canvas has no size yet, wait for it to be ready
        if canvas_width <= 1 or canvas_height <= 1:
            self.canvas.after(100, lambda: self.draw_state(state))
            return

        # Calculate cell size
        cell_width = canvas_width / (state.width + 2)
        cell_height = canvas_height / (state.height + 2)
        cell_size = min(cell_width, cell_height)

        # Round the cell size to prevent fractional pixels
        cell_size = int(cell_size)

        # Resize images with slightly larger dimensions to prevent gaps
        padding = 1  # Add 1 pixel padding to prevent gaps
        image_size = cell_size + padding * 2
        try:
            self.wall_photo = ImageTk.PhotoImage(self.wall_image.resize((image_size, image_size), Image.LANCZOS))
            self.stone_photo = ImageTk.PhotoImage(self.stone_image.resize((image_size, image_size), Image.LANCZOS))
            self.ares_photo = ImageTk.PhotoImage(self.ares_image.resize((image_size, image_size), Image.LANCZOS))
            self.switch_photo = ImageTk.PhotoImage(self.switch_image.resize((image_size, image_size), Image.LANCZOS))
            self.empty_photo = ImageTk.PhotoImage(self.empty_image.resize((image_size, image_size), Image.LANCZOS))
            self.surround_photo = ImageTk.PhotoImage(self.surround_image.resize((image_size, image_size), Image.LANCZOS))
        except Exception as e:
            return

        # Calculate offsets for centering
        x_offset = (canvas_width - (state.width * cell_size)) / 2
        y_offset = (canvas_height - (state.height * cell_size)) / 2

        # Round the offsets to prevent fractional pixels
        x_offset = int(x_offset)
        y_offset = int(y_offset)

        # Draw background first
        for y in range(state.height):
            for x in range(state.width):
                # Calculate exact pixel positions
                x1 = x_offset + x * cell_size
                y1 = y_offset + y * cell_size

                # Draw empty background for all cells
                self.canvas.create_image(
                    x1 + cell_size // 2,
                    y1 + cell_size // 2,
                    image=self.empty_photo,
                    anchor=tk.CENTER
                )

        # Draw game elements
        for y in range(state.height):
            for x in range(state.width):
                # Calculate exact pixel positions
                x1 = x_offset + x * cell_size
                y1 = y_offset + y * cell_size

                # Draw walls
                if (x, y) in state.walls:
                    self.canvas.create_image(
                        x1 + cell_size // 2,
                        y1 + cell_size // 2,
                        image=self.wall_photo,
                        anchor=tk.CENTER
                    )

                # Draw switches
                if (x, y) in state.switches:
                    self.canvas.create_image(
                        x1 + cell_size // 2,
                        y1 + cell_size // 2,
                        image=self.surround_photo,
                        anchor=tk.CENTER
                    )
                    self.canvas.create_image(
                        x1 + cell_size // 2,
                        y1 + cell_size // 2,
                        image=self.switch_photo,
                        anchor=tk.CENTER
                    )

                # Draw stones
                if (x, y) in state.stones:
                    self.canvas.create_image(
                        x1 + cell_size // 2,
                        y1 + cell_size // 2,
                        image=self.stone_photo,
                        anchor=tk.CENTER
                    )
                    # Draw stone weight if it exists
                    weight = state.stones.get((x, y), 0)
                    if weight > 0:
                        self.canvas.create_text(
                            x1 + cell_size // 2,
                            y1 + cell_size // 2,
                            text=str(weight),
                            fill='white',
                            font=('Helvetica', max(int(cell_size / 3), 12))
                        )

                # Draw player
                if hasattr(state, 'player_pos') and state.player_pos == (x, y):
                    self.canvas.create_image(
                        x1 + cell_size // 2,
                        y1 + cell_size // 2,
                        image=self.ares_photo,
                        anchor=tk.CENTER
                    )
