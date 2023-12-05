import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Set up the figure and axes for the animation
fig, ax = plt.subplots()
bar_labels = ['Hulls in Progress', 'Hulls Completed', 'Turrets in Progress', 'Turrets Completed']
bars = ax.bar(bar_labels, [0, 0, 0, 0])

# Set some properties for the plot
ax.set_ylim(0, max([max([d[key] for key in d]) for d in parsed_data]) + 1)
ax.set_ylabel('Count')
ax.set_title('Simulation Progress of Hulls and Turrets')

# Define the update function for the animation
def update(frame):
    data = parsed_data[frame]
    for bar, label in zip(bars, bar_labels):
        bar.set_height(data[label.lower().replace(' ', '_')])
    return bars

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(parsed_data), blit=True, repeat=False)
