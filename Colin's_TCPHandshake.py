# Made by Colin Mckay on April 17, 2025.
# Purpose: Visualize the 3-way handshake using tkinter


"""
Colin's_tcphandshake.py - Visual TCP 3-Way Handshake using tkinter
"""

import tkinter as tk
import time
import threading


class TCPHandshakeVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title('Colin\'s 3-Way TCP Handshake Visualizer')
        self.root.configure(bg="#1e1e2e")

        self.canvas = tk.Canvas(root, width=600, height=300, bg="#1e1e2e", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.log_box = tk.Text(root, width=40, height=20, bg="#2a2a3d", fg="#8ecae6", font=("Courier", 10))
        self.log_box.grid(row=0, column=1, padx=(0, 10), pady=10)
        self.log_box.insert(tk.END, ">> Log initialized...\n")

        self.start_btn = tk.Button(root, text="Start Handshake", command=self.run_handshake, bg="#3a3a5c", fg="white")
        self.start_btn.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        self.client_x, self.client_y = 100, 70
        self.server_x, self.server_y = 500, 70
        self.dot_radius = 15

    def log(self, message):
        self.log_box.insert(tk.END, f">> {message}\n")
        self.log_box.see(tk.END)

    def draw_nodes(self):
        # Draw client (blue) and server (green) nodes
        self.canvas.create_oval(
            self.client_x - self.dot_radius, self.client_y - self.dot_radius,
            self.client_x + self.dot_radius, self.client_y + self.dot_radius,
            fill="cyan", outline=""
        )
        self.canvas.create_text(self.client_x, self.client_y + 30, text="Client", fill="white",
                                font=("Gothic", 10, "bold"))

        self.canvas.create_oval(
            self.server_x - self.dot_radius, self.server_y - self.dot_radius,
            self.server_x + self.dot_radius, self.server_y + self.dot_radius,
            fill="lime green", outline=""
        )
        self.canvas.create_text(self.server_x, self.server_y + 30, text="Server", fill="white",
                                font=("Gothic", 10, "bold"))

    def animate_message(self, x1, y1, x2, y2, color, label, delay):
        steps = 30
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps
        message_radius = 8

        for i in range(steps + 1):
            x = x1 + dx * i
            y = y1 + dy * i
            msg = self.canvas.create_oval(
                x - message_radius, y - message_radius,
                x + message_radius, y + message_radius,
                fill=color, outline=""
            )
            self.root.update()
            time.sleep(delay)
            if i != steps:
                self.canvas.delete(msg)

        self.log(f"{label} sent")

    def run_handshake(self):
        threading.Thread(target=self._run_handshake_sequence).start()

    def _run_handshake_sequence(self):
        self.canvas.delete("all")
        self.draw_nodes()

        time.sleep(1)
        self.animate_message(self.client_x, self.client_y, self.server_x, self.server_y, "yellow", "SYN", 0.05)

        time.sleep(1)
        self.animate_message(self.server_x, self.server_y, self.client_x, self.client_y, "lime", "SYN-ACK", 0.05)

        time.sleep(1)
        self.animate_message(self.client_x, self.client_y, self.server_x, self.server_y, "cyan", "ACK", 0.05)

        time.sleep(1)
        self.log("Connection established!")
        self.canvas.create_text(300, 220, text="Connection Established!", fill="white", font=("Helvetica", 12, "bold"))


# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    app = TCPHandshakeVisualizer(root)
    root.mainloop()
