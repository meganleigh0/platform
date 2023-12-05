import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Function to parse the log data
def parse_log_data(log_df):
    counts = {
        "hulls_in_progress": 0,
        "hulls_completed": 0,
        "turrets_in_progress": 0,
        "turrets_completed": 0,
    }
    history = []
    for _, row in log_df.iterrows():
        interaction = row["Interaction"]
        if "Start Plant 1 Hull" in interaction:
            counts["hulls_in_progress"] += 1
        elif "Start Plant 1 Turret" in interaction:
            counts["turrets_in_progress"] += 1
        elif "Complete Plant 1 Hull" in interaction:
            counts["hulls_in_progress"] -= 1
            counts["hulls_completed"] += 1
        elif interaction == "Hull Status":
            counts["hulls_in_progress"] = row.get("InProcessing", 0)
            counts["hulls_completed"] = row.get("Completed", 0)
        history.append(counts.copy())
    return history

parsed_data = parse_log_data(log_df)

# Set up the figure and axes for the animation
fig, ax = plt.subplots()
bar_labels = ['Hulls in Progress', 'Hulls Completed', 'Turrets in Progress', 'Turrets Completed']
bars = ax.bar(bar_labels, [0, 0, 0, 0])
ax.set_ylim(0, max([max([d[key] for key in d]) for d in parsed_data]) + 1)
ax.set_ylabel('Count')
ax.set_title('Simulation Progress of Hulls and Turrets')

# Update function for the animation
def update(frame):
    data = parsed_data[frame]
    for bar, label in zip(bars, bar_labels):
        bar.set_height(data[label.lower().replace(' ', '_')])
    return bars

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(parsed_data), blit=True, repeat=False)

# Save the animation as a video file
ani.save('simulation_progress.mp4', writer='ffmpeg', fps=1)

# Display the plot (for interactive environments)
plt.show()
