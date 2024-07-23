import plotly.express as px
import pandas as pd

# Assuming you have loaded your DataFrame, replace 'df' with your DataFrame variable
# Example DataFrame creation for demonstration
data = {
    'Operation': ['SCAVENGE MANIFOLD', 'WATER SEPARATOR', 'FUEL PUMP', 'FILTER'],
    'Start Time': [0.000000, 0.275862, 0.551724, 0.827586],
    'End Time': [8.076832, 8.039420, 8.043148, 8.333181],
    'Station': ['STA 11', 'STA 11', 'STA 11', 'STA 11'],
    'Vehicle': ['Hull 3', 'Hull 3', 'Hull 3', 'Hull 3']
}
df = pd.DataFrame(data)

# Convert the time to a proper datetime format
# Here assuming times are in hours and converting them to timedelta
df['Start Time'] = pd.to_timedelta(df['Start Time'], unit='h')
df['End Time'] = pd.to_timedelta(df['End Time'], unit='h')

# For plotting, we need a reference date, assuming all times are relative to the same day
reference_date = pd.Timestamp('2024-07-01')
df['Start Time'] = reference_date + df['Start Time']
df['End Time'] = reference_date + df['End Time']

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