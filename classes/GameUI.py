import tkinter as tk
from tkinter import ttk
import os

from .GameState import GameState
from .SokobanSolver import SokobanSolver

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ares Stone Game")

        # Initialize all variables first
        self.selected_algorithm = tk.StringVar(value = "bfs")
        self.current_state = None
        self.solver = None
        self.is_playing = False
        self.is_solved = False
        self.current_step = 0
        self.weight_var = tk.StringVar(value="Total Weight: 0       Step: 0")
        self.play_speed = 250  # milliseconds between moves
        self.old_selection = None # Store old selection when changing algorithm

        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles
        style.configure('Sidebar.TFrame', background='#2c3e50')
        style.configure('Game.TFrame', background='#ecf0f1')
        style.configure('Controls.TFrame', background='#ecf0f1')
        style.configure('Modern.TButton', padding = 10, font=('Helvetica', 10))
        style.configure('Modern.TLabel', background = '#2c3e50', foreground='white', font = ('Helvetica', 11))
        style.configure('Controls.TLabel', background = '#ecf0f1', font = ('Helvetica', 12))

        # Configure main window
        self.root.geometry("1280x720")
        self.root.configure(bg = '#ecf0f1')

        # Create main container
        self.main_container = ttk.Frame(self.root, style='Game.TFrame')
        self.main_container.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 20)

        # Create frames
        self.create_left_sidebar()
        self.create_game_display()
        self.create_right_sidebar()
        self.create_controls()

    def create_left_sidebar(self):
        sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=250)
        sidebar.pack(side = tk.LEFT, fill = tk.Y, padx = (0, 20))
        sidebar.pack_propagate(False)

        title_label = ttk.Label(sidebar, text="Level Selection", style='Modern.TLabel', font=('Helvetica', 14, 'bold'))
        title_label.pack(pady = (20, 10), padx = 10)

        list_container = ttk.Frame(sidebar, style='Sidebar.TFrame')
        list_container.pack(fill = tk.BOTH, expand = True, padx = 10, pady = (0, 20))

        self.input_listbox = tk.Listbox(
            list_container,
            font = ('Helvetica', 11),
            bg = '#34495e',
            fg = 'white',
            selectmode = tk.SINGLE,
            relief = tk.FLAT,
            highlightthickness = 0,
            selectbackground = '#3498db',
            selectforeground = 'white',
            borderwidth = 0
        )

        scrollbar = ttk.Scrollbar(list_container, orient = tk.VERTICAL, command = self.input_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_listbox.pack(side = tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_listbox.config(yscrollcommand = scrollbar.set)

        for i in range(1, 11):
            self.input_listbox.insert(tk.END, f" Level {i:02d}")

        self.input_listbox.bind('<<ListboxSelect>>', self.load_input_file)

    def create_right_sidebar(self):
        sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=250)
        sidebar.pack(side=tk.RIGHT, fill = tk.Y, padx = (20, 0))
        sidebar.pack_propagate(False)

        title_label = ttk.Label(sidebar, text="Algorithm Selection", style='Modern.TLabel', font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(20, 10), padx = 10)

        # Create listbox container
        list_container = ttk.Frame(sidebar, style='Sidebar.TFrame')
        list_container.pack(fill=tk.BOTH, expand = True, padx = 10, pady = (0, 20))

        # Create listbox for algorithms
        self.algorithm_listbox = tk.Listbox(
            list_container,
            font=('Helvetica', 11),
            bg='#34495e',
            fg='white',
            selectmode=tk.SINGLE,
            relief=tk.FLAT,
            highlightthickness = 0,
            selectbackground = '#3498db',
            selectforeground = 'white',
            borderwidth = 0,
            height = 2
        )

        # Add algorithms to listbox
        algorithms = [" Breadth-First Search", " Depth-First Search"]
        for alg in algorithms:
            self.algorithm_listbox.insert(tk.END, alg)

        # Select BFS by default
        self.algorithm_listbox.select_set(0)

        # Bind selection event
        self.algorithm_listbox.bind('<<ListboxSelect>>', self.on_algorithm_select)
        self.algorithm_listbox.pack(fill = tk.BOTH, expand = True)

    def on_algorithm_select(self, event):
        selection = self.algorithm_listbox.curselection()
        if selection:
            # Map selection to algorithm value
            alg_map = {0: "bfs", 1: "dfs"}
            prev_algorithm = self.selected_algorithm.get()
            new_algorithm = alg_map[selection[0]]

            if prev_algorithm != new_algorithm:
                self.selected_algorithm.set(new_algorithm)
                self.load_input_file(None, True)
                self.reset_solve_state()

    def create_game_display(self):
        game_frame = ttk.Frame(self.main_container, style = 'Game.TFrame')
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand = True)

        self.canvas = tk.Canvas(game_frame,
                                bg = '#ffffff',
                                highlightthickness = 0,
                                relief = tk.FLAT)
        self.canvas.pack(fill = tk.BOTH, expand = True)

    def create_controls(self):
        controls = ttk.Frame(self.root, style='Controls.TFrame')
        controls.pack(side = tk.BOTTOM, fill=tk.X, padx = 20, pady = 20)

        # Create container for buttons and weight
        control_container = ttk.Frame(controls, style='Controls.TFrame')
        control_container.pack(anchor='center')

        # Button frame
        button_frame = ttk.Frame(control_container, style='Controls.TFrame')
        button_frame.pack()

        self.solve_button = ttk.Button(button_frame,
                                    text="Solve Puzzle",
                                    style='Modern.TButton',
                                    command=self.solve_puzzle,
                                    width = 15)
        self.solve_button.pack(side=tk.LEFT, padx = 5)

        self.play_button = ttk.Button(button_frame,
                                    text = "Play",
                                    style='Modern.TButton',
                                    command=self.toggle_play,
                                    width=15,
                                    state='disabled')
        self.play_button.pack(side = tk.LEFT, padx = 5)

        self.next_button = ttk.Button(button_frame,
                                    text = "Next Step",
                                    style = 'Modern.TButton',
                                    command = self.next_step,
                                    width = 15,
                                    state = 'disabled')
        self.next_button.pack(side=tk.LEFT, padx = 5)

        # Weight label
        weight_label = ttk.Label(control_container,
                            textvariable = self.weight_var,
                            font = ('Helvetica', 12),
                            style = 'Controls.TLabel')
        weight_label.pack(pady = (10, 0))

    # Show error popup with custom message
    def show_error_popup(self, message):
        popup = tk.Toplevel(self.root)
        popup.title("Error")

        # Calculate position to center the popup
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 50
        popup.geometry(f"400x100+{x}+{y}")

        # Configure popup
        popup.transient(self.root)
        popup.grab_set()

        # Add message
        msg_label = ttk.Label(popup, text = message, wraplength = 350, justify = 'center')
        msg_label.pack(expand = True, pady = 10)

        # Add OK button
        ok_button = ttk.Button(popup, text = "OK", command=popup.destroy)
        ok_button.pack(pady = (0, 10))

    def load_input_file(self, event, new_slection = False):
        selection = self.input_listbox.curselection()
        if new_slection:
            selection = self.old_selection
        self.old_selection = selection

        if not selection:
            return

        file_num = selection[0] + 1
        filename = f"input-{file_num:02d}.txt"

        try:
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    weights = list(map(int, file.readline().rstrip('\n').split()))
                    map_temp = []
                    for line in file:
                        map_temp.append(list(line.rstrip('\n')))

                    n = len(map_temp[0])
                    m = len(map_temp)
                    # print(n, " ", m)
                    weight_data = [[0 for _ in range(m)] for _ in range(n)]
                    map_data = [[' ' for _ in range(m)] for _ in range(n)]
                    weight_id = 0

                    for j in range(m):
                        for i in range(n):
                            map_data[i][j] = map_temp[j][i]
                            if map_temp[j][i] in ['$', '*']:
                                weight_data[i][j] = weights[weight_id]
                                weight_id += 1

                    # for j in range(m):
                    #     for i in range(n):
                    #         print(map_data[i][j], end = ' ')
                    #     print()
                    # for j in range(m):
                    #     for i in range(n):
                    #         print(weight_data[i][j], end = ' ')
                    #     print()

                    self.current_state = GameState(map_data, weight_data)
                    self.solver = None
                    self.draw_state(self.current_state)
            else:
                print(f"File {filename} not found")
        except Exception as e:
            print(f"Error loading file: {e}")
        self.reset_solve_state()

    # Reset the solve state when algorithm or input changes
    def reset_solve_state(self):
        self.is_solved = False
        self.is_playing = False
        self.solver = None
        self.total_weight = 0
        self.current_step = 0
        self.weight_var.set("Total Weight: 0       Step: 0")
        self.solve_button.config(state = 'normal')
        self.play_button.config(text = "Play", state = 'disabled')
        self.next_button.config(state = 'disabled')

    def solve_puzzle(self):
        if not self.current_state:
            return

        self.solver = SokobanSolver(self.current_state)
        algorithm = self.selected_algorithm.get()

        solved = False
        if algorithm == "bfs":
            solved = self.solver.solve_bfs()
        elif algorithm == "dfs":
            solved = self.solver.solve_dfs()

        if solved:
            # print("Solution found")
            self.is_solved = True
            self.play_button.config(state = 'normal')
            self.next_button.config(state = 'normal')
            self.solve_button.config(state = 'disabled')
        else:
            self.show_error_popup("Cannot solve the puzzle after 1000000 (1e6) operations.")
            self.solve_button.config(state = 'disabled')

    def next_step(self):
        if not self.solver or not self.current_state or not self.is_solved:
            return False

        next_move = self.solver.get_next_step()
        if next_move:
            dy, dx = next_move
            player_pos = self.current_state.find_player()
            if player_pos:
                y, x = player_pos
                if self.solver.can_move(self.current_state, y, x, dy, dx):
                    # Check if moving stone
                    new_y, new_x = y + dy, x + dx
                    target_cell = self.current_state.get_cell(new_y, new_x)

                    # Update total weight and total step
                    self.total_weight += 1
                    self.current_step += 1

                    if target_cell in ['$', '*']:
                        # Get weight of stone being pushed
                        stone_weight = self.current_state.get_weight(new_y, new_x)
                        self.total_weight += stone_weight

                    self.weight_var.set(f"Total Weight: {self.total_weight}       Step: {self.current_step}")

                    # Make the move
                    self.current_state = self.solver.make_move(self.current_state, y, x, dy, dx)
                    self.draw_state(self.current_state)
                    return True
        return False

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
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill = colors['#'], width = 0)
                elif char in ['$', '*']:
                    self.canvas.create_oval(x1p, y1p, x2p, y2p,
                                        fill = colors['$'],
                                        width = 0)
                    if char == '*':
                        self.canvas.create_oval(x1p, y1p, x2p, y2p,
                                            outline = colors['.'],
                                            width = 2)
                    # Only draw weight for stones
                    weight = state.get_weight(x, y)
                    if weight > 0:
                        text_x = (x1 + x2) / 2
                        text_y = (y1 + y2) / 2
                        self.canvas.create_text(text_x, text_y,
                                            text = str(weight),
                                            fill = 'white',
                                            font = ('Helvetica', int(cell_size / 3)))
                elif char == '@':
                    self.canvas.create_oval(x1p, y1p, x2p, y2p,
                                        fill = colors['@'],
                                        width = 0)
                elif char == '.':
                    self.canvas.create_oval(x1p, y1p, x2p, y2p,
                                        fill = colors['.'],
                                        width = 0)
                elif char == '+':
                    self.canvas.create_oval(x1p, y1p, x2p, y2p,
                                        fill = colors['@'],
                                        outline = colors['.'],
                                        width = 3)

    def toggle_play(self):
        if not self.is_solved:
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_button.config(text = "Pause")
            self.next_button.config(state = 'disabled')
            self.auto_play()
        else:
            self.play_button.config(text = "Play")
            self.next_button.config(state = 'normal')

    def auto_play(self):
        if self.is_playing:
            has_next = self.next_step()
            if has_next:
                self.root.after(self.play_speed, self.auto_play)
            else:
                # No more steps then stop playing
                self.is_playing = False
                self.play_button.config(text = "Play")
                self.next_button.config(state = 'normal')

    def update_display(self, event = None):
        if self.current_state:
            self.draw_state(self.current_state)
