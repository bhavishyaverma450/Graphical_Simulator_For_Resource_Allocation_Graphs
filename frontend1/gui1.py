import sys
import os

# Update import statements
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from backend.deadlock_detection import detect_deadlock
from backend.visualization import visualize_graph

class ResourceAllocationGraph:
    def __init__(self, master):
        self.master = master
        self.master.title("Resource Allocation Graph Simulator")
        
        # Create main container
        self.main_container = ttk.Frame(self.master)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self.main_container, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create button frame with better styling
        self.button_frame = ttk.Frame(self.main_container, padding="5 5 5 5")
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.nodes = {}
        self.edges = []
        self.node_positions = {}
        self.selected_node = None

        # Add buttons with improved styling
        ttk.Label(self.button_frame, text="Controls", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        self.add_process_button = ttk.Button(self.button_frame, text="Add Process", command=self.add_process)
        self.add_process_button.pack(pady=5, fill=tk.X)

        self.add_resource_button = ttk.Button(self.button_frame, text="Add Resource", command=self.add_resource)
        self.add_resource_button.pack(pady=5, fill=tk.X)

        self.create_edge_button = ttk.Button(self.button_frame, text="Create Edge", command=self.create_edge)
        self.create_edge_button.pack(pady=5, fill=tk.X)

        self.clear_button = ttk.Button(self.button_frame, text="Clear All", command=self.clear_all)
        self.clear_button.pack(pady=5, fill=tk.X)

        self.start_button = ttk.Button(self.button_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(pady=20, fill=tk.X)

        # Add status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.master, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind canvas events
        self.canvas.tag_bind("node", "<Button-1>", self.node_clicked)
        self.canvas.tag_bind("node", "<B1-Motion>", self.node_dragged)
        self.canvas.tag_bind("node", "<ButtonRelease-1>", self.node_released)
        self.canvas.tag_bind("node", "<Enter>", self.node_hover_enter)
        self.canvas.tag_bind("node", "<Leave>", self.node_hover_leave)

    def node_clicked(self, event):
        self.selected_node = self.canvas.find_closest(event.x, event.y)[0]
        self.last_x = event.x
        self.last_y = event.y

    def node_dragged(self, event):
        if self.selected_node:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.canvas.move(self.selected_node, dx, dy)
            # Move associated text label
            self.canvas.move(self.selected_node + 1, dx, dy)
            # Update edge positions
            self.update_edges()
            self.last_x = event.x
            self.last_y = event.y

    def node_released(self, event):
        if self.selected_node:
            # Update node position in storage
            coords = self.canvas.coords(self.selected_node)
            node_id = self.canvas.gettags(self.selected_node)[1]  # Get node ID from tags
            center_x = (coords[0] + coords[2]) / 2
            center_y = (coords[1] + coords[3]) / 2
            self.node_positions[node_id] = (center_x, center_y)
        self.selected_node = None

    def node_hover_enter(self, event):
        node_id = self.canvas.gettags(self.canvas.find_closest(event.x, event.y)[0])[1]
        self.status_var.set(f"Node: {node_id}")

    def node_hover_leave(self, event):
        self.status_var.set("Ready")

    def update_edges(self):
        # Update all edge positions when nodes are moved
        for edge in self.canvas.find_withtag("edge"):
            tags = self.canvas.gettags(edge)
            from_node = tags[1]
            to_node = tags[2]
            x1, y1 = self.node_positions[from_node]
            x2, y2 = self.node_positions[to_node]
            self.canvas.coords(edge, x1, y1, x2, y2)

    def clear_all(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.edges.clear()
        self.node_positions.clear()
        self.status_var.set("Cleared all nodes and edges")

    def add_process(self):
        process_id = simpledialog.askstring("Input", "Enter Process ID:")
        if process_id:
            x, y = self.get_next_position()
            self.nodes[process_id] = 'process'
            self.node_positions[process_id] = (x, y)
            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill='lightblue', tags=(process_id, "node"))
            self.canvas.create_text(x, y, text=process_id, tags=(process_id, "label"))
            print(f"Process {process_id} added at position ({x}, {y}).")

    def add_resource(self):
        resource_id = simpledialog.askstring("Input", "Enter Resource ID:")
        if resource_id:
            x, y = self.get_next_position()
            self.nodes[resource_id] = 'resource'
            self.node_positions[resource_id] = (x, y)
            self.canvas.create_rectangle(x-25, y-25, x+25, y+25, fill='lightgreen', tags=(resource_id, "node"))
            self.canvas.create_text(x, y, text=resource_id, tags=(resource_id, "label"))
            print(f"Resource {resource_id} added at position ({x}, {y}).")

    def create_edge(self):
        from_node = simpledialog.askstring("Input", "Enter From Node ID:")
        to_node = simpledialog.askstring("Input", "Enter To Node ID:")
        if from_node and to_node and from_node in self.nodes and to_node in self.nodes:
            self.edges.append((from_node, to_node))
            x1, y1 = self.node_positions[from_node]
            x2, y2 = self.node_positions[to_node]
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, tags=("edge", from_node, to_node))
            print(f"Edge created from {from_node} to {to_node}.")

    def get_next_position(self):
        # Simple layout algorithm to position nodes
        num_nodes = len(self.node_positions)
        x = 100 + (num_nodes % 8) * 80
        y = 100 + (num_nodes // 8) * 80
        return x, y

    def start_simulation(self):
        print("Starting simulation...")
        print(f"Nodes: {self.nodes}")
        print(f"Edges: {self.edges}")
        deadlock = detect_deadlock(self.nodes, self.edges)
        print(f"Deadlock detected: {deadlock}")
        visualize_graph(self.nodes, self.edges, deadlock)
        if deadlock:
            messagebox.showwarning("Deadlock Detected", "A deadlock has been detected in the graph!")
        print("Simulation complete.")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    app = ResourceAllocationGraph(root)
    root.mainloop()
