# Multi-Agent SDN Controller using Reinforcement Learning

## Project Overview

This project implements a **Multi-Agent Software Defined Networking (SDN) Controller** that uses **Reinforcement Learning (RL)** to optimize network traffic management.

The system is built using **Mininet for network simulation** and a **custom controller implemented in Python**. Multiple intelligent agents monitor network conditions and dynamically adjust routing decisions to improve performance.

## Key Features

* Multi-agent architecture for SDN control
* Reinforcement Learning-based traffic optimization
* Real-time network monitoring
* Web dashboard for visualization
* Network simulation using Mininet

## Technologies Used

* Python
* Mininet
* SDN Controller
* Reinforcement Learning
* Web Dashboard (Flask / Python)

## Project Structure

multi-agent-sdn-controller
│
├── agents/
│   └── rl_agent.py
│
├── controller/
│   ├── main_controller.py
│   └── baseline_controller.py
│
├── topology/
│   └── topology.py
│
├── web_dashboard.py
│
└── README.md

## How to Run the Project

### 1. Clone the Repository

git clone https://github.com/Snehalatha29/multi-agent-sdn-controller.git

### 2. Navigate to the Project Folder

cd multi-agent-sdn-controller

### 3. Run Mininet Topology

sudo python3 mininet/topology.py

### 4. Start the Controller

python3 controller/main_controller.py

### 5. Launch Web Dashboard

python3 web_dashboard.py

## Sample Output

The system tests connectivity between hosts using Mininet:

Example:
h1 -> h2 h3
h2 -> h1 h3
h3 -> h1 h2

Results: **0% packet loss**

## Future Improvements

* Advanced RL algorithms
* Traffic prediction using AI
* Improved visualization dashboard
* Real-time network analytics

## Author

Snehalatha Mekala
Final Year B.Tech Project

GitHub: https://github.com/Snehalatha29
