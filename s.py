import plotly.graph_objects as go

# Unique list of stations
stations = grouped_data['Station'].unique()

# Create a figure with Plotly
fig = go.Figure()

# Function to update the graph based on the selected station
def create_station_trace(station):
    station_data = grouped_data[grouped_data['Station'] == station]
    for department in station_data['Department'].unique():
        df = station_data[station_data['Department'] == department]
        fig.add_trace(
            go.Bar(
                x=df['AssemblyID'],
                y=df['Hours'],
                name=department,
                visible=(station == stations[0])  # Only the first station is visible by default
            )
        )

# Adding traces for each station
for station in stations:
    create_station_trace(station)

# Dropdown menus
buttons = [
    dict(
        label=station,
        method="update",
        args=[{"visible": [station == s for s in stations for _ in grouped_data['Department'].unique()]},
              {"title": f"Total Hours by Department and Assembly: {station}"}]
    ) for station in stations
]

# Adding dropdown to the layout
fig.update_layout(
    updatemenus=[dict(active=0, buttons=buttons)],
    title=f"Total Hours by Department and Assembly: {stations[0]}",
    xaxis_title='Assembly ID',
    yaxis_title='Total Hours'
)

# Showing the figure
fig.show()
