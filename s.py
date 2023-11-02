import pandas as pd
import plotly.graph_objects as go

# Sample DataFrame (replace this with your actual dataframe)
df = pd.DataFrame({
    'Assembly': ['plate', 'plate'],
    'Station': ['p1', 'p1'],
    'Timestamp_start': [0.00, 0.00],
    'Timestamp_end': [1.00, 1.00],
    'Vehicle': ['va1', 'va2']
})

# Get a list of unique vehicles to generate a color map
vehicles = df['Vehicle'].unique()
colors = px.colors.qualitative.Plotly
vehicle_color_map = {vehicle: colors[i % len(colors)] for i, vehicle in enumerate(vehicles)}

# Create a unique list of stations for the dropdown
stations = df['Station'].unique()
stations.sort()

# Function to create traces for each station
def create_traces_for_station(df, station=None):
    traces = []
    filtered_df = df if station is None else df[df['Station'] == station]
    for _, row in filtered_df.iterrows():
        color = vehicle_color_map[row['Vehicle']]
        traces.append(
            go.Bar(
                x=[row['Timestamp_end'] - row['Timestamp_start']],
                y=[f"{row['Assembly']} - {row['Station']}"],
                base=row['Timestamp_start'],
                name=row['Vehicle'],
                orientation='h',
                marker=dict(color=color),
            )
        )
    return traces

# Create traces for all stations
all_station_traces = create_traces_for_station(df)

# Initialize figure with the traces for all stations
fig = go.Figure(data=all_station_traces)

# Create the dropdown options
dropdown_options = [
    {'label': 'All Stations', 'method': 'update', 'args': [{'visible': [True] * len(all_station_traces)}]}
]

for station in stations:
    station_traces = create_traces_for_station(df, station)
    # Visibility list - True for the current station's traces, False for others
    visibility = [True if trace.name == station else False for trace in all_station_traces]
    
    dropdown_option = {
        'label': station,
        'method': 'update',
        'args': [{'visible': visibility}]
    }
    dropdown_options.append(dropdown_option)

# Add dropdown
fig.update_layout(
    updatemenus=[{
        'buttons': dropdown_options,
        'direction': 'down',
        'showactive': True,
    }],
    title="Gantt Chart by Station and Vehicle",
    xaxis_title="Time",
    yaxis_title="Assembly - Station",
    barmode='stack',
    showlegend=False  # Hide legend if not required
)

# Show the figure
fig.show()
