import tkinter as tk
from tkinter import ttk
import Visualize

def visualize(process_table, algorithm):
    # Function to visualize the processes based on the selected algorithm
    process_dict = {}
    process_list = []
    arriv_time_list = []
    burst_time_list = []
    priority_list = []
    for item in process_table.get_children():
        values = process_table.item(item)['values']
        process_list.append(values[0])
        arriv_time_list.append(values[1])
        burst_time_list.append(values[2])
        priority_list.append(values[3])
    process_dict = {
        'Process': process_list,
        'Arrival Time': arriv_time_list,
        'Burst Time': burst_time_list,
        'Priority': priority_list
    }
    Visualize.visualize(process_dict, algorithm)

def add_process():
    # Function to add a new process to the table
    process_number = process_number_entry.get()
    arrival_time = arrival_time_entry.get()
    burst_time = burst_time_entry.get()
    priority = priority_entry.get()
    process_table.insert("", tk.END, values=(process_number, arrival_time, burst_time, priority))
    process_number_entry.delete(0, tk.END)
    arrival_time_entry.delete(0, tk.END)
    burst_time_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)

def remove_process():
    # Function to remove the selected process from the table
    selected_item = process_table.selection()
    process_table.delete(selected_item)

# Create the main window
window = tk.Tk()
window.title("Scheduling Visualization")
window.geometry("800x600")

# Apply a custom style to the window
style = ttk.Style(window)
style.theme_use("clam")

# Create radio buttons for scheduling algorithms
algorithm_label = tk.Label(window, text="Select Scheduling Algorithm:", font=("Arial", 12, "bold"))
algorithm_label.pack()

algorithm_var = tk.StringVar()
algorithm_var.set("FCFS")

algorithms = ["FCFS", "SJF", "SRT", "Priority", "Round Robin"]
for algorithm in algorithms:
    algorithm_radio = tk.Radiobutton(window, text=algorithm, variable=algorithm_var, value=algorithm, font=("Arial", 10))
    algorithm_radio.pack()

# Create a table for process details
table_frame = tk.Frame(window)
table_frame.pack(pady=20)

process_table = ttk.Treeview(table_frame, columns=("Process Number", "Arrival Time", "Burst Time", "Priority"), show="headings")
process_table.heading("Process Number", text="Process Number")
process_table.heading("Arrival Time", text="Arrival Time")
process_table.heading("Burst Time", text="Burst Time")
process_table.heading("Priority", text="Priority")

process_table.column("Process Number", width=100, anchor=tk.CENTER)
process_table.column("Arrival Time", width=100, anchor=tk.CENTER)
process_table.column("Burst Time", width=100, anchor=tk.CENTER)
process_table.column("Priority", width=100, anchor=tk.CENTER)

process_table.pack(side="left", padx=10)

# Add separator lines between table columns
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
style.configure("Treeview", font=("Arial", 10))
style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
style.configure("Treeview.Heading", background="gray", foreground="white", relief="raised", bordercolor="black")
style.configure("Treeview", bordercolor="black", relief="sunken")

separator_style = ttk.Style()
separator_style.configure("Separator.TSeparator", background="black")
separator = ttk.Separator(table_frame, orient="vertical", style="Separator.TSeparator")
separator.pack(side="left", fill="y", padx=5)


# Create entry fields for process details
entry_frame = tk.Frame(window)
entry_frame.pack(pady=10)

process_number_label = tk.Label(entry_frame, text="Process Number:", font=("Arial", 10))
process_number_label.grid(row=0, column=0, padx=10)
process_number_entry = tk.Entry(entry_frame)
process_number_entry.grid(row=0, column=1, padx=10)

arrival_time_label = tk.Label(entry_frame, text="Arrival Time:", font=("Arial", 10))
arrival_time_label.grid(row=1, column=0, padx=10)
arrival_time_entry = tk.Entry(entry_frame)
arrival_time_entry.grid(row=1, column=1, padx=10)

burst_time_label = tk.Label(entry_frame, text="Burst Time:", font=("Arial", 10))
burst_time_label.grid(row=2, column=0, padx=10)
burst_time_entry = tk.Entry(entry_frame)
burst_time_entry.grid(row=2, column=1, padx=10)

priority_label = tk.Label(entry_frame, text="Priority:", font=("Arial", 10))
priority_label.grid(row=3, column=0, padx=10)
priority_entry = tk.Entry(entry_frame)
priority_entry.grid(row=3, column=1, padx=10)

add_button = tk.Button(entry_frame, text="Add Process", command=add_process, font=("Arial", 10, "bold"), bg="green", fg="white")
add_button.grid(row=4, column=0, pady=10)
remove_button = tk.Button(entry_frame, text="Remove Process", command=remove_process, font=("Arial", 10, "bold"), bg="red", fg="white")
remove_button.grid(row=4, column=1, pady=10)

# Create a button to visualize the processes
visualize_button = tk.Button(window, text="Visualize", command=lambda: visualize(process_table, algorithm_var.get()), font=("Arial", 12, "bold"), bg="blue", fg="white", padx=20, pady=10)
visualize_button.pack()

# Start the Tkinter event loop
window.mainloop()
