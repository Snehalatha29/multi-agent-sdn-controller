import sqlite3
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("database/traffic_logs.db")
c = conn.cursor()

# Fetch data
c.execute("SELECT latency, bandwidth FROM logs")
rows = c.fetchall()

if not rows:
    print("No data found. Run pingall multiple times first.")
    exit()

latency = [r[0] for r in rows]
bandwidth = [r[1] for r in rows]

# Plot graph
plt.figure(figsize=(8, 4))
plt.plot(latency, label="Latency (ms)")
plt.plot(bandwidth, label="Bandwidth Usage (%)")

plt.title("Network Metrics Over Time")
plt.xlabel("Samples")
plt.ylabel("Value")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("results_graph.png", dpi=300)
print("Graph saved as results_graph.png")

