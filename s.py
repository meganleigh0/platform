import pandas as pd
import plotly.graph_objects as go

# Data
data = {
    'Time': [0.00, 0.00, 1.00, 1.00, 2.00, 2.00],
    'Interaction': ['Starting assy 1', 'Starting assy 2', 'Completed assy 1', 'Starting assy 1', 'Completed assy 2', 'Started assy 2'],
    'ID': [101, 102, 101, 101, 102, 102],
    'Vehicle': [1, 1, 1, 2, 1, 2],
    'Section': ['p1', 'p1', 'p1', 'p1', 'p1', 'p1']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create the figure
fig = go.Figure()

# Loop through each unique combination of assembly ID and vehicle
for (ID, vehicle), group in df.groupby(['ID', 'Vehicle']):
    # Check if we have both start and end points
    if group.shape[0] == 2:
        fig.add_trace(go.Scatter(x=group['Time'], y=group['ID'],
                                 mode='lines+markers',
                                 name=f"Vehicle {vehicle}, ID {ID}"))

# Adjust layout
fig.update_layout(title='Assembly Interactions over Time',
                  xaxis_title='Time',
                  yaxis_title='Assembly ID')

# Show the figure
fig.show()