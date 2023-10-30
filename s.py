import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Sample dataframe
data = {'AssemblyID': [1, 2, 1, 2, 1, 2, 1, 2],
        'Interaction': ['start', 'start', 'end', 'end', 'start', 'start', 'end', 'end'],
        'Station': ['station 1', 'station 2', 'station 1', 'station 2', 'station 1', 'station 2', 'station 1', 'station 2'],
        'Timestamp': [0.000, 0.000, 2.000, 3.000, 3.000, 5.000, 8.000, 9.000],
        'Vehicle': [1, 1, 1, 1, 2, 2, 2, 2]}

df = pd.DataFrame(data)

fig, ax = plt.subplots()
stations = df['Station'].unique()
num_stations = len(stations)

# Create a dictionary to map stations to y-values
station_dict = {station: i for i, station in enumerate(stations)}

# Plot initialization function
def init():
    ax.clear()
    ax.set_xlim(0, df['Timestamp'].max() + 2)
    ax.set_ylim(0, num_stations)
    ax.set_yticks(range(num_stations))
    ax.set_yticklabels(stations)
    ax.set_xlabel('Time')
    ax.set_title('Vehicles Moving Through Stations')

# Update function for the animation
def update(frame):
    ax.clear()
    current_time = frame / 10  # Adjust this for faster/slower animation
    ongoing_df = df[df['Timestamp'] <= current_time]
    
    for _, row in ongoing_df.iterrows():
        y = station_dict[row['Station']]
        if row['Interaction'] == 'start':
            color = 'green'
        else:
            color = 'red'
        ax.scatter(row['Timestamp'], y, color=color, label=row['Vehicle'])
    
    ax.set_xlim(0, df['Timestamp'].max() + 2)
    ax.set_ylim(0, num_stations)
    ax.set_yticks(range(num_stations))
    ax.set_yticklabels(stations)
    ax.set_xlabel('Time')
    ax.set_title('Vehicles Moving Through Stations at time {:.2f}'.format(current_time))

ani = FuncAnimation(fig, update, frames=int(df['Timestamp'].max()*10 + 20), init_func=init, blit=False, repeat=True)
plt.tight_layout()
plt.show()