import os
import asyncio
import tkinter as tk
from tkinter import ttk
from .GameState import GameState
from .algorithms.BFS import BFSSolver
from .algorithms.DFS import DFSSolver
from .algorithms.UCS import UCSSolver
from .algorithms.A_Star import AStarSolver

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
        self.current_task = None

        self.setup_bindings()
        self.load_level("1")

    def setup_bindings(self):
        self.gui.selected_level.trace_add('write', lambda *args: self.on_level_change())
        self.gui.selected_algorithm.trace_add('write', lambda *args: self.on_algorithm_change())
        self.gui.solve_button.config(command=self.start_solve)
        self.gui.play_button.config(command=self.toggle_play)
        self.gui.next_button.config(command=self.next_step)
        self.gui.root.bind('<Configure>', self.update_display)

    def load_level(self, level_num):
        filename = f"input-{int(level_num):02d}.txt"

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
                    self.gui.draw_state(self.current_state)
            else:
                print(f"File {filename} not found")
        except Exception as e:
            print(f"Error loading file: {e}")

        self.reset_solve_state()

    def on_level_change(self):
        if self.current_task:
            # Cancel any running solve task
            self.current_task.cancel()
            self.current_task = None
        level = self.gui.selected_level.get()
        self.reset_full_state()
        self.load_level(level)

    def on_algorithm_change(self):
        if self.current_task:
            # Cancel any running solve task
            self.current_task.cancel()
            self.current_task = None
        self.stop_playback()
        self.reset_full_state()
        level = self.gui.selected_level.get()
        self.load_level(level)

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

    async def solve_puzzle(self):
        if not self.current_state:
            return

        try:
            if self.gui.selected_algorithm.get() == "bfs":
                self.solver = BFSSolver(self.current_state)
                data_structure = self.solver.queue
            elif self.gui.selected_algorithm.get() == "dfs":
                self.solver = DFSSolver(self.current_state)
                data_structure = self.solver.stack
            elif self.gui.selected_algorithm.get() == "ucs":
                self.solver = UCSSolver(self.current_state)
                data_structure = self.solver.priority_queue
            else:
                self.solver = AStarSolver(self.current_state)
                data_structure = self.solver.priority_queue

            operations = 0
            chunk_size = 1000

            while operations < self.solver.operation_limit:
                for _ in range(chunk_size):
                    operations += 1
                    if self.solver.process_one_state():
                        self.is_solved = True
                        # Show play and next buttons, hide solve button
                        self.gui.solve_button.pack_forget()
                        self.gui.play_button.pack(side=tk.LEFT, padx=5)
                        self.gui.next_button.pack(side=tk.LEFT, padx=5)

                        # Save metrics after successful solve
                        level_number = self.gui.selected_level.get()
                        self.solver.save_metrics(level_number)
                        return True

                    if not data_structure:
                        break

                # Yield control to prevent freezing
                await asyncio.sleep(0)

            self.show_error_popup("Cannot solve the puzzle after 1,000,000 operations.")
            self.gui.solve_button.pack_forget()
            return False

        # Clean up when task is cancelled
        except asyncio.CancelledError:
            self.solver = None
            self.gui.solve_button.config(text="Solve Puzzle")
            self.gui.solve_button.pack(side=tk.LEFT, padx=5)
            # Re-raise to properly handle cancellation
            raise

    def start_solve(self):
        if self.current_task:
            self.current_task.cancel()
        self.current_task = asyncio.create_task(self.solve_puzzle())
        self.gui.solve_button.config(text="Solving...")
        self.gui.solve_button.config(state='disabled')

    def reset_solve_state(self):
        if self.current_task:
            self.current_task.cancel()
            self.current_task = None

        self.is_playing = False
        self.is_solved = False
        self.solver = None
        self.current_step = 0
        self.total_weight = 0

        self.gui.weight_var.set("Total Weight: 0       Step: 0")
        # Show solve button
        self.gui.solve_button.pack(side=tk.LEFT, padx=5)
        self.gui.solve_button.config(text="Solve Puzzle")
        self.gui.solve_button.config(state='normal')
        # Unpack play and next buttons if they were packed
        self.gui.play_button.pack_forget()
        self.gui.next_button.pack_forget()
        self.gui.play_button.config(state='normal')
        self.gui.next_button.config(state='normal')

    def reset_full_state(self):
        self.current_state = None
        self.reset_solve_state()

    def stop_playback(self):
        if self.is_playing:
            self.is_playing = False
            self.gui.play_button.config(text="Play")
            # Show next button
            self.gui.next_button.pack(side=tk.LEFT, padx=5)

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
        else:
            self.gui.play_button.config(state='disabled')
            self.gui.next_button.config(state='disabled')
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
                # Store the after ID so we can cancel it if needed
                self.gui.root.after(self.play_speed, self.auto_play)
            else:
                # No more steps then stop playing
                self.stop_playback()

    def update_display(self, event=None):
        if self.current_state:
            self.gui.draw_state(self.current_state)
