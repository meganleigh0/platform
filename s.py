import plotly.express as px
import pandas as pd

# Sample DataFrame
data = {
    'Operation': ['Op1', 'Op2', 'Op3', 'Op4'],
    'Start Time': ['2024-07-01 08:00:00', '2024-07-01 09:00:00', '2024-07-01 10:00:00', '2024-07-01 11:00:00'],
    'End Time': ['2024-07-01 09:00:00', '2024-07-01 10:00:00', '2024-07-01 11:00:00', '2024-07-01 12:00:00'],
    'Station': ['S1', 'S2', 'S1', 'S3'],
    'Vehicle': ['V1', 'V2', 'V1', 'V3']
}
df = pd.DataFrame(data)

# Convert time columns to datetime
df['Start Time'] = pd.to_datetime(df['Start Time'])
df['End Time'] = pd.to_datetime(df['End Time'])

# Create Gantt chart using Plotly Express
fig = px.timeline(df, x_start="Start Time", x_end="End Time", y="Station", color="Vehicle", title='Operation Timeline')

# Update layout
fig.update_layout(
    xaxis_title='Time',
    yaxis_title='Station',
    yaxis={'categoryorder': 'total ascending'}
)

# Show the plot
fig.show()