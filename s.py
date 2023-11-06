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

# Group and aggregate data
agg_df = df.groupby(['Vehicle', 'Station'])[['Timestamp_start', 'Timestamp_end']].agg({'Timestamp_start': 'min', 'Timestamp_end': 'max'}).reset_index()

# Assign unique colors to each vehicle
colors = {vehicle: f'rgb({hash(vehicle) % 256}, {hash(vehicle*2) % 256}, {hash(vehicle*3) % 256})' for vehicle in df['Vehicle'].unique()}

# Initialize figure
fig = go.Figure()

for vehicle in agg_df['Vehicle'].unique():
    color = colors[vehicle]
    vehicle_data = agg_df[agg_df['Vehicle'] == vehicle]
    
    # Create the Gantt chart bars
    fig.add_trace(go.Bar(
        x=vehicle_data['Timestamp_end'] - vehicle_data['Timestamp_start'],  # Duration of the task
        y=vehicle_data['Station'],
        name=vehicle,
        orientation='h',
        marker=dict(color=color),
        text=vehicle_data['Vehicle'],  # Display the vehicle name
        hoverinfo='text+name',
    ))

# Update layout
fig.update_layout(
    title='Assembly Schedule by Station',
    xaxis_title='Time',
    yaxis_title='Station',
    barmode='stack',
    bargap=0.1,
    legend_title_text='Vehicle'
)

# Show the figure
fig.show()