import plotly.graph_objects as go

# Create an empty figure
fig = go.Figure()

# Iterate through the merged_df to plot each line segment
for i, row in merged_df.iterrows():
    fig.add_trace(go.Scatter(x=[row['Start_Time'], row['End_Time']],
                             y=[row['AssemblyID'], row['AssemblyID']],
                             mode='lines',
                             line=dict(color=f'rgba({255*(1-row["Vehicle"])},0,{255*row["Vehicle"]},0.5)'),  # Just a simple way to color by vehicle
                             name=f"Vehicle {row['Vehicle']}"))

# Updating the layout to add a title and labels
fig.update_layout(title='Assembly over time',
                  xaxis_title='Time',
                  yaxis_title='Assembly ID')

# Show the plot
fig.show()