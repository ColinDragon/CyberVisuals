# Created by Colin Mckay on April 17, 2025.
# Purpose: Create a program that simulates a man in the middle attack and shows it to the user visually.

import tkinter as tk
import threading


class MITMStepVisualizer:
    def __init__(self, master):
        """Initialize the visualization window and setup basic configuration."""
        self.master = master
        self.master.title("Colin's MITM Visualizer")  # Window title
        self.master.geometry("800x600")  # Window size
        self.master.config(bg="#1e1e1e")  # Background color

        # Grid configuration for better resizing
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=0)

        # Canvas for drawing nodes and messages
        self.canvas = tk.Canvas(self.master, bg="#2e2e2e", width=480, height=600, highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # sticky makes canvas resize

        # Log Text Box for event logs
        self.log_box = tk.Text(self.master, width=40, height=20, bg="#2a2a3d", fg="#8ecae6", font=("Courier", 10))
        self.log_box.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")  # sticky for resizing
        self.log_box.insert(tk.END, ">> Log initialized...\n")  # Initial log message
        self.log_box.config(wrap="word")  # Ensure word wrapping in the log box

        # Start simulation button
        self.start_button = tk.Button(self.master, text="Start MITM Simulation", command=self.start_simulation,
                                      bg="#ff4d4d", fg="white", font=("Arial", 12, "bold"))
        self.start_button.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10)

        # Status label for simulation
        self.status_label = tk.Label(self.master, text="Status: Waiting to start...", fg="white", bg="#1e1e1e",
                                     font=("Arial", 12), wraplength=400)
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky="nsew")
        self.status_label.config(justify="center")  # Center the text inside the label

        # Node positions
        self.client_x, self.client_y = 100, 70
        self.attacker_x, self.attacker_y = 250, 250
        self.bob_x, self.bob_y = 400, 430
        self.dot_radius = 20

        self.setup_nodes()  # Setup initial nodes

    def log(self, message, color="white"):
        """Logs a message to the log box with the specified color."""
        self.log_box.insert(tk.END, f">> {message}\n")  # Insert message
        self.log_box.see(tk.END)  # Scroll to the end
        self.log_box.tag_add("start", "1.0", "end")  # Apply tag for color
        self.log_box.tag_config("start", foreground=color)  # Set color

    def setup_nodes(self):
        """Draw the key nodes: Alice, Attacker, and Bob."""
        # Alice
        self.canvas.create_oval(self.client_x - self.dot_radius, self.client_y - self.dot_radius,
                                self.client_x + self.dot_radius, self.client_y + self.dot_radius, fill="#5dade2", tags="alice")
        self.canvas.create_text(self.client_x, self.client_y + 30, text="Alice", fill="white", font=("Arial", 12))

        # Attacker
        self.canvas.create_oval(self.attacker_x - self.dot_radius, self.attacker_y - self.dot_radius,
                                self.attacker_x + self.dot_radius, self.attacker_y + self.dot_radius, fill="#f1948a", tags="attacker")
        self.canvas.create_text(self.attacker_x, self.attacker_y + 30, text="Attacker", fill="white", font=("Arial", 12))

        # Bob
        self.canvas.create_oval(self.bob_x - self.dot_radius, self.bob_y - self.dot_radius,
                                self.bob_x + self.dot_radius, self.bob_y + self.dot_radius, fill="#58d68d", tags="bob")
        self.canvas.create_text(self.bob_x, self.bob_y + 30, text="Bob", fill="white", font=("Arial", 12))

    def animate_message(self, from_x, from_y, to_x, to_y, color, label, delay):
        """Animates a message sent from one node to another with smooth motion."""
        steps = 30  # Number of animation steps
        dx = (to_x - from_x) / steps  # Change in x per step
        dy = (to_y - from_y) / steps  # Change in y per step
        message_radius = 8  # Message circle radius

        # Animate message
        for i in range(steps + 1):
            x = from_x + dx * i
            y = from_y + dy * i
            msg = self.canvas.create_oval(x - message_radius, y - message_radius, x + message_radius, y + message_radius,
                                          fill=color, outline="", tags="message")  # Draw message
            self.master.update()  # Update GUI
            self.master.after(50)  # Schedule next frame to avoid freezing
            if i != steps:  # Delete message if it's not the last step
                self.canvas.delete(msg)

        self.log(f"{label} sent", color)  # Log message

    def run_simulation(self):
        """Runs the MITM simulation in a separate thread."""
        threading.Thread(target=self.simulate_steps, daemon=True).start()  # Run simulation in background thread

    def simulate_steps(self):
        """Performs the MITM simulation with step-by-step animations."""
        # Step-by-step simulation with status updates
        self.update_status("Alice is sending a message to Attacker...")

        # Step 1: Client → Attacker (SYN)
        self.animate_message(self.client_x, self.client_y, self.attacker_x, self.attacker_y, "yellow", "SYN", 0.05)
        self.master.after(1000)  # Wait for animation completion

        # Step 2: Attacker modifies message (SYN-ACK)
        self.update_status("Attacker intercepts and modifies the message...")
        self.animate_message(self.attacker_x, self.attacker_y, self.client_x, self.client_y, "lime", "SYN-ACK", 0.05)
        self.master.after(1000)

        # Step 3: Attacker → Bob (SYN-ACK)
        self.update_status("Attacker sends modified message to Bob...")
        self.animate_message(self.attacker_x, self.attacker_y, self.bob_x, self.bob_y, "red", "Modified SYN-ACK", 0.05)
        self.master.after(1000)

        # Step 4: Bob → Attacker (ACK)
        self.update_status("Bob sends ACK to Attacker...")
        self.animate_message(self.bob_x, self.bob_y, self.attacker_x, self.attacker_y, "cyan", "ACK", 0.05)
        self.master.after(1000)

        # Step 5: Attacker → Alice (Fake ACK)
        self.update_status("Attacker sends fake ACK to Alice...")
        self.animate_message(self.attacker_x, self.attacker_y, self.client_x, self.client_y, "orange", "Fake ACK", 0.05)
        self.master.after(1000)

        self.log("Simulation Complete! MITM attack sequence finished.")
        self.update_status("MITM attack simulation complete.")  # Final status

    def update_status(self, message):
        """Updates the status label in a thread-safe manner."""
        self.status_label.config(text=f"Status: {message}")

    def start_simulation(self):
        """Resets the canvas and starts the simulation."""
        self.canvas.delete("all")  # Clear canvas
        self.setup_nodes()  # Redraw nodes
        self.run_simulation()  # Start the simulation


if __name__ == "__main__":
    root = tk.Tk()
    app = MITMStepVisualizer(root)
    root.mainloop()  # Run the main GUI loop
