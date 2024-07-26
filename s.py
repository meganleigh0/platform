import plotly.express as px
import pandas as pd

df = operation_df.copy()

# Convert the time columns to float if they are not already
df['Start Time'] = df['Start Time'].astype(float)
df['End Time'] = df['End Time'].astype(float)

# Convert the time to a proper timedelta format
df['Start Time'] = pd.to_timedelta(df['Start Time'], unit='h')
df['End Time'] = pd.to_timedelta(df['End Time'], unit='h')

# For plotting, we need a reference date, assuming all times are relative to the same day
reference_date = pd.Timestamp('2024-07-01')
df['Start Time'] = reference_date + df['Start Time']
df['End Time'] = reference_date + df['End Time']

# Create Gantt chart using Plotly Express
fig = px.timeline(df, x_start="Start Time", x_end="End Time", y="Station", color="Vehicle", title='Operation Timeline')

fig.show()
