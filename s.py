import pandas as pd
import plotly.graph_objs as go

# Create the DataFrame
df = pd.DataFrame({
    'Assembly': ['box', 'wheel', 'tire', 'tire', 'tire', 'toy'],
    'Station': ['Station 1', 'Station 1', 'Station 1', 'Station 2', 'Station 2', 'Station 2'],
    'Timestamp_start': [0.00, 0.00, 1.00, 2.00, 5.00, 5.00],
    'Timestamp_end': [1.00, 1.00, 3.00, 4.00, 7.00, 7.00],
    'Vehicle': ['bus1', 'car1', 'bus1', 'bus1', 'bus1', 'car1']
})

# Assign unique colors to each vehicle
colors = {vehicle: f'rgb({hash(vehicle) % 256}, {hash(vehicle*2) % 256}, {hash(vehicle*3) % 256})' for vehicle in df['Vehicle'].unique()}

# Initialize figure
fig = go.Figure()

# Track the vehicles added to the legend
legend_added = []

for vehicle, group in df.groupby('Vehicle'):
    color = colors[vehicle]
    # For each vehicle, add all its corresponding bars
    for i, row in group.iterrows():
        showlegend = False

        # If the vehicle is not in the legend, add it
        if vehicle not in legend_added:
            showlegend = True
            legend_added.append(vehicle)

        # Create the bar for the Gantt chart
        fig.add_trace(go.Bar(
            x=[row['Timestamp_end'] - row['Timestamp_start']],  # Duration of the task
            y=[row['Station']],
            name=vehicle,  # This will put the vehicle name in the legend
            orientation='h',
            marker=dict(color=color),
            showlegend=showlegend,
            legendgroup=vehicle,  # Group by vehicle for the legend
            width=0.4,  # You can adjust the width for better spacing
            base=row['Timestamp_start'],  # Start time of the task
            text=row['Assembly'],  # The assembly name written on the bar
            hoverinfo='text+name',  # Show both vehicle and assembly as hover info
        ))

# Update layout
fig.update_layout(
    title='Assembly Schedule by Station',
    xaxis_title='Time',
    yaxis_title='Station',
    barmode='stack',
    bargap=0.1,  # Gap between bars of adjacent location coordinates.
    legend_title_text='Vehicle'
)

# Show the figure
fig.show()



# Filter DataFrame for Station 1 only
df_station1 = df[df['Station'] == 'Station 1']

# Assign unique colors to each vehicle
colors = {vehicle: f'rgb({hash(vehicle) % 256}, {hash(vehicle*2) % 256}, {hash(vehicle*3) % 256})' for vehicle in df_station1['Vehicle'].unique()}

# Initialize figure
fig = go.Figure()

# Track the vehicles added to the legend
legend_added = []

for index, row in df_station1.iterrows():
    vehicle = row['Vehicle']
    color = colors[vehicle]
    showlegend = False

    # If the vehicle is not in the legend, add it
    if vehicle not in legend_added:
        showlegend = True
        legend_added.append(vehicle)

    # Create the bar for the bar chart
    fig.add_trace(go.Bar(
        x=[row['Timestamp_end'] - row['Timestamp_start']],  # Duration of the task
        y=[row['Assembly']],  # Use Assembly as the y-axis category
        name=vehicle,  # This will put the vehicle name in the legend
        orientation='h',
        marker=dict(color=color),
        showlegend=showlegend,
        width=0.4,  # You can adjust the width for better spacing
        base=row['Timestamp_start'],  # Start time of the task
        hoverinfo='text+name',  # Show both vehicle and assembly as hover info
    ))

# Update layout
fig.update_layout(
    title='Station 1 Assembly Schedule',
    xaxis_title='Time',
    yaxis_title='Assembly',
    barmode='stack',
    bargap=0.1,  # Gap between bars of adjacent location coordinates.
    legend_title_text='Vehicle'
)

# Show the figure
fig.show()
