import pygame
import random
import time
from collections import deque
from tkinter import messagebox

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
processes = deque()
completed = deque()


# Process class
class Process:
    def __init__(self, id, arrival_time, burst_time, priority=None):
        self.index = id
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.start_time = 0
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.x = 0
        self.y = 0
        self.width = self.burst_time * 10
        self.executing = False
        self.arrived = False

    def execute(self, time_quantum, window):
        global completed
        if self.start_time > time_quantum:
            return
        if self.burst_time + self.start_time > time_quantum:
            if not self.arrived:
                self.arrived = True
                self.x = time_quantum * 10
                self.y = HEIGHT // 2 - 15 + self.index * 50
            self.width = time_quantum * 10
        if self.burst_time + self.start_time <= time_quantum:
            self.executing = False
            completed.append(self)
            print(list(completed))
            print(f"Process {self.id} executed successfully")
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, 30), border_radius=5)

    def draw_completed(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, 30), border_radius=5)


# Create processes for different scheduling algorithms
def create_processes(data, algorithm):
    global processes
    algorithm = algorithm.lower()
    if algorithm == 'fcfs':
        for i in range(len(data['Process'])):
            processes.append(Process(i, data['Arrival Time'][i], data['Burst Time'][i]))
    elif algorithm == 'sjf':
        sorted_indices = sorted(range(len(data['Burst Time'])), key=lambda k: data['Burst Time'][k])
        for i, index in enumerate(sorted_indices):
            processes.append(Process(i, data['Arrival Time'][index], data['Burst Time'][index]))
    elif algorithm == 'priority_np' or algorithm=="priority":
        sorted_indices = sorted(range(len(data['Priority'])), key=lambda k: data['Priority'][k])
        for i, index in enumerate(sorted_indices):
            processes.append(Process(i, data['Arrival Time'][index], data['Burst Time'][index], data['Priority'][index]))
    elif algorithm == 'priority_p':
        for i in range(len(data['Process'])):
            processes.append(Process(i, data['Arrival Time'][i], data['Burst Time'][i], data['Priority'][i]))
    elif algorithm == 'srtf':
        sorted_indices = sorted(range(len(data['Burst Time'])), key=lambda k: data['Burst Time'][k])
        for i, index in enumerate(sorted_indices):
            processes.append(Process(i, data['Arrival Time'][index], data['Burst Time'][index]))
    elif algorithm == 'rr':
        for i in range(len(data['Process'])):
            processes.append(Process(i, data['Arrival Time'][i], data['Burst Time'][i]))


# Display time quantum on top
def display_time_quantum(time_quantum):
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Time Quantum: {time_quantum}", True, BLACK)
    window.blit(text, (10, 10))


# Display completed processes in bottom right
def display_completed():
    global completed, window
    title = pygame.font.SysFont(None, 30)
    for i in range(len(completed)):
        font = pygame.font.SysFont(None, 25)
        text = font.render(
            f"Process {i}: Arrival Time={completed[i].arrival_time}, Burst Time={completed[i].burst_time}",
            True, BLACK)
        window.blit(text, (10, 50 + i * 25))
        completed[i].draw_completed(window)


def increase_time_quantum():
    global time_quantum
    time_quantum += 1


# Main game loop
def game_loop(algorithm):
    global time_quantum, completed, processes, window

    clock = pygame.time.Clock()
    running = True
    time_quantum = 1  # Set a default time quantum
    increase_interval = 1  # Increase time quantum every 1 second
    last_increase_time = time.time()
    current_process = None  # Currently executing process
    is_completed = False
    show_dialog_box = True

    # Set timer event for increasing time quantum
    pygame.time.set_timer(pygame.USEREVENT, increase_interval * 1000)

    while running:
        # Process input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    time_quantum += 1  # Increase time quantum with up arrow key
                elif event.key == pygame.K_DOWN:
                    time_quantum = max(time_quantum - 1, 1)  # Decrease time quantum with down arrow key (minimum of 1)
            elif event.type == pygame.USEREVENT:
                if not is_completed:
                    current_time = time.time()
                    if current_time - last_increase_time >= increase_interval:
                        increase_time_quantum()
                        last_increase_time = current_time

        # Clear the screen
        window.fill(WHITE)

        # Display time quantum
        display_time_quantum(time_quantum)

        # Draw the grid background
        draw_grid_background()

        # Display completed processes
        display_completed()

        # Check if there is a process currently executing
        if current_process is None or not current_process.executing:
            # Check if there are pending processes in the queue
            if processes and processes[0].arrival_time <= time_quantum:
                current_process = processes.popleft()
                current_process.start_time = time_quantum
                current_process.executing = True

        # Execute the current process
        if current_process and current_process.executing:
            current_process.execute(time_quantum, window)

        # Update the display
        pygame.display.update()
        clock.tick(30)  # FPS

        if len(processes) == 0 and current_process.executing is False and show_dialog_box:
            # Display simulation complete message
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer event
            messagebox.showinfo("Simulation Complete", "Simulation has been completed.")
            is_completed = True
            show_dialog_box = False

    pygame.quit()


def draw_grid_background():
    # Calculate the maximum width and height of the rectangles
    max_width = window.get_width() - 60
    max_height = 30  # Height of the rectangles

    # Calculate the starting position of the grid
    start_x = 10
    start_y = 250

    # Calculate the ending position of the grid
    end_x = start_x + max_width
    end_y = start_y + 10 * max_height

    # Draw the grid lines and time labels
    grid_spacing = 50  # Distance between grid lines
    for x in range(start_x, end_x + grid_spacing, grid_spacing):
        pygame.draw.line(window, BLACK, (x, start_y), (x, end_y), 1)
        time_label = str((x - start_x) // (grid_spacing // 2) * 1.5)
        font = pygame.font.SysFont(None, 15)
        text = font.render(time_label, True, BLACK)
        text_rect = text.get_rect(center=(x, end_y + 20))
        window.blit(text, text_rect)

    for y in range(start_y, end_y + max_height, max_height):
        pygame.draw.line(window, BLACK, (start_x, y), (end_x, y), 1)


def visualize(data, algorithm):
    # Initialize Pygame
    pygame.init()
    global window, processes, completed

    # Set up the display
    processes = deque()
    completed = deque()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CPU Scheduling Visualization")

    # Draw the grid background
    draw_grid_background()

    create_processes(data, algorithm)
    game_loop(algorithm)


# def main():
#     # Provide sample data for visualization
#     data = {
#         'Process': ['P1', 'P2', 'P3', 'P4', 'P5'],
#         'Arrival Time': [0, 1, 3, 5, 6],
#         'Burst Time': [6, 4, 2, 3, 5],
#         'Priority': [3, 1, 4, 2, 5]
#     }

#     # Choose the algorithm ('FCFS', 'SJF', 'Priority', 'PriorityPreemptive', 'SRT', 'RR')
#     algorithm = 'FCFS'

#     visualize(data, algorithm)


# if __name__ == '__main__':
#     main()
