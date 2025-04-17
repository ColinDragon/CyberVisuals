# CyberVisuals

MITM Attack Visualizer is a Python-based tool designed to simulate and visually demonstrate a Man-in-the-Middle (MITM) attack. Built with Tkinter, this tool enables users to observe the attack process in real-time with an interactive and intuitive GUI.

Features
Interactive Visualization: Step-by-step animation of a MITM attack.
Live Logs: Real-time event logs that track the attack’s progress.
Minimalist Design: Focuses on clarity and ease of use.
Professional Interface: Clean layout, optimized for both visual appeal and functionality.

How It Works
Attack Simulation: Visualizes the MITM attack with clear animations for each step.
Log Output: Events are logged in real-time, with color-coded messages for clarity.
Smooth Animations: Message transitions are animated with fluid motion.
Threaded Execution: The simulation runs on a separate thread, ensuring the interface remains responsive.

Simulation Steps
Step 1: Alice (Client) sends a SYN to the attacker.
Step 2: The attacker sends a modified SYN-ACK to Alice.
Step 3: The attacker forwards the SYN-ACK to Bob (Server).
Step 4: Bob sends an ACK to the attacker.
Step 5: The attacker sends a fake ACK back to Alice.

Installation
Install Python 3.x from python.org.
Clone the Repository:

bash - > Copy - > Edit
git clone https://github.com/yourusername/mitm-attack-visualizer.git
cd mitm-attack-visualizer
Run the Program:

bash - > Copy - > Edit
python mitm_visualizer.py

Contributing
Contributions are welcome! Open an issue or submit a pull request to enhance the tool.

