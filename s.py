import pandas as pd
import plotly.express as px

# Assume operation_df is your DataFrame
df = operation_df.copy()

# Convert the time columns to float if they are not already
df['Start'] = df['Start'].astype(float)
df['End'] = df['End'].astype(float)

# Create Gantt chart using Plotly Express with hours as continuous values
fig = px.timeline(df, x_start="Start", x_end="End", y="Station", color="Hull", title="Operation Timeline")

# Customize the x-axis to reflect hours
fig.update_layout(xaxis_title='Hours')

# Show the plot
fig.show()