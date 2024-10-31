import os
import tkinter as tk
from tkinter import ttk
from .GameState import GameState
from .algorithms.BFS import BFSSolver
from .algorithms.DFS import DFSSolver

class Core:
    def __init__(self, gui):
        self.gui = gui
        self.current_state = None
        self.solver = None
        self.is_playing = False
        self.is_solved = False
        self.current_step = 0
        self.total_weight = 0
        self.play_speed = 200
        self.old_selection = None
        self.new_selection = False
        self.selected_algorithm = "bfs"

        self.setup_bindings()

    def setup_bindings(self):
        self.gui.input_listbox.bind('<<ListboxSelect>>', self.load_input_file)
        self.gui.algorithm_listbox.bind('<<ListboxSelect>>', self.on_algorithm_select)
        self.gui.solve_button.config(command=self.solve_puzzle)
        self.gui.play_button.config(command=self.toggle_play)
        self.gui.next_button.config(command=self.next_step)
        self.gui.root.bind('<Configure>', self.update_display)

    def show_error_popup(self, message):
        popup = tk.Toplevel(self.gui.root)
        popup.title("Error")
        x = self.gui.root.winfo_x() + (self.gui.root.winfo_width() // 2) - 200
        y = self.gui.root.winfo_y() + (self.gui.root.winfo_height() // 2) - 50
        popup.geometry(f"400x100+{x}+{y}")
        popup.transient(self.gui.root)
        popup.grab_set()

        msg_label = ttk.Label(popup, text=message, wraplength=350, justify='center')
        msg_label.pack(expand=True, pady=10)

        ok_button = ttk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=(0, 10))

    def load_input_file(self, event):
        selection = self.input_listbox.curselection()
        # print(self.new_slection, self.old_selection, selection)
        if self.new_slection == True:
            selection = self.old_selection
        self.old_selection = selection
        # print(self.new_slection, self.old_selection, selection)

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

    def on_algorithm_select(self, event):
        selection = self.algorithm_listbox.curselection()
        if selection:
            alg_map = {0: "bfs", 1: "dfs"}
            prev_algorithm = self.selected_algorithm.get()
            new_algorithm = alg_map[selection[0]]

            # print(prev_algorithm, " ", new_algorithm)
            if prev_algorithm != new_algorithm:
                self.selected_algorithm.set(new_algorithm)
                self.new_slection = True
                self.load_input_file(None)
                self.new_slection = False

    def solve_puzzle(self):
        if not self.current_state:
            return

        if self.selected_algorithm == "bfs":
            self.solver = BFSSolver(self.current_state)
        else:
            self.solver = DFSSolver(self.current_state)

        if self.solver.solve():
            self.is_solved = True
            self.gui.play_button.config(state='normal')
            self.gui.next_button.config(state='normal')
            self.gui.solve_button.config(state='disabled')
        else:
            self.show_error_popup("Cannot solve the puzzle after 1000000 (1e6) operations.")
            self.gui.solve_button.config(state='disabled')

    def reset_solve_state(self):
            """Reset all solving-related state variables"""
            self.is_solved = False
            self.is_playing = False
            self.solver = None
            self.total_weight = 0
            self.current_step = 0
            self.gui.weight_var.set("Total Weight: 0       Step: 0")
            self.gui.solve_button.config(state='normal')
            self.gui.play_button.config(text="Play", state='disabled')
            self.gui.next_button.config(state='disabled')

    def load_input_file(self, event):
        selection = self.gui.input_listbox.curselection()

        if self.new_selection:
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
                    weight_data = [[0 for _ in range(m)] for _ in range(n)]
                    map_data = [[' ' for _ in range(m)] for _ in range(n)]
                    weight_id = 0

                    for j in range(m):
                        for i in range(n):
                            map_data[i][j] = map_temp[j][i]
                            if map_temp[j][i] in ['$', '*']:
                                weight_data[i][j] = weights[weight_id]
                                weight_id += 1

                    self.current_state = GameState(map_data, weight_data)
                    self.solver = None
                    self.gui.draw_state(self.current_state)
            else:
                print(f"File {filename} not found")
        except Exception as e:
            print(f"Error loading file: {e}")

        self.reset_solve_state()

    # Execute the next step in the solution
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

                    self.gui.weight_var.set(f"Total Weight: {self.total_weight}       Step: {self.current_step}")

                    # Make the move
                    self.current_state = self.solver.make_move(self.current_state, y, x, dy, dx)
                    self.gui.draw_state(self.current_state)
                    return True
        return False

    # Toggle between play and pause states
    def toggle_play(self):
        if not self.is_solved:
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.gui.play_button.config(text="Pause")
            self.gui.next_button.config(state='disabled')
            self.auto_play()
        else:
            self.gui.play_button.config(text="Play")
            self.gui.next_button.config(state='normal')

    def auto_play(self):
        if self.is_playing:
            has_next = self.next_step()
            if has_next:
                self.gui.root.after(self.play_speed, self.auto_play)
            else:
                # No more steps then stop playing
                self.is_playing = False
                self.gui.play_button.config(text="Play")
                self.gui.next_button.config(state='normal')

    def update_display(self, event=None):
        if self.current_state:
            self.gui.draw_state(self.current_state)
