import time
import psutil
import os

class AlgorithmMetrics:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.start_memory = None
        self.end_memory = None
        self.nodes_explored = 0
        self.total_steps = 0
        self.total_weight = 0
        self.solution_path = ""

    def start_tracking(self):
        self.start_time = time.time()
        self.start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

    def stop_tracking(self):
        self.end_time = time.time()
        self.end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

    def get_execution_time_ms(self):
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0

    def get_memory_usage_mb(self):
        if self.start_memory and self.end_memory:
            return self.end_memory - self.start_memory
        return 0

    def format_solution_path(self):
        # Add space between each move character
        return ' '.join(list(self.solution_path))

    def save_to_file(self, algorithm_name, level_number):
        output_filename = f"output-{int(level_number):02d}.txt"

        # Use 'a' mode to append to the file
        with open(output_filename, 'a') as f:
            # If file is empty then will not add an extra newline at the start
            if os.path.getsize(output_filename) > 0:
                f.write('\n')
            f.write(f"{algorithm_name}\n")
            f.write(f"Steps: {self.total_steps}, Weight: {self.total_weight}, ")
            f.write(f"Nodes: {self.nodes_explored}, ")
            f.write(f"Time (ms): {self.get_execution_time_ms():.2f}, ")
            f.write(f"Memory (MB): {self.get_memory_usage_mb():.2f}\n")
            f.write(self.format_solution_path())
