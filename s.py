import plotly.graph_objects as go
import numpy as np

# Using the previously processed 'final_df'

# Create a unique color list for vehicles
color_list = ['#'+ ''.join([np.random.choice(list('0123456789ABCDEF')) for j in range(6)]) for i in range(len(final_df['Vehicle'].unique()))]
color_dict = dict(zip(final_df['Vehicle'].unique(), color_list))

fig = go.Figure()

# Add a trace for each vehicle
for vehicle, color in color_dict.items():
    vehicle_df = final_df[final_df['Vehicle'] == vehicle].sort_values(by=['Timestamp_start'])

    x_values = []
    y_values = []
    for _, row in vehicle_df.iterrows():
        x_values.extend([row['Timestamp_start'], row['Timestamp_end'], None])  # 'None' creates a gap
        y_values.extend([row['Station'], row['Station'], None])  # 'None' creates a gap

    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        name=f'Vehicle {vehicle}',
        line=dict(width=10, color=color)
    ))

fig.update_layout(
    title='Assembly Interactions by Vehicle and Station',
    xaxis_title='Timestamp',
    yaxis_title='Station',
    yaxis_categoryorder='total descending'
)

fig.show()
