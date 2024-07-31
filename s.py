import pandas as pd
import plotly.express as px
import numpy as np
from datetime import timedelta
import holidays

# Assume operation_df is your DataFrame
df = operation_df.copy()

# Convert the time columns to float if they are not already
df['Start'] = df['Start'].astype(float)
df['End'] = df['End'].astype(float)

# Convert the time to a proper timedelta format
df['Start'] = pd.to_timedelta(df['Start'], unit='h')
df['End'] = pd.to_timedelta(df['End'], unit='h')

# Define a function to adjust for working days
us_holidays = holidays.US()

def adjust_for_working_days(start_date, timedelta_hours):
    total_days = timedelta_hours // 24
    remaining_hours = timedelta_hours % 24
    adjusted_date = np.busday_offset(start_date, total_days, holidays=us_holidays)
    adjusted_date = pd.Timestamp(adjusted_date) + timedelta(hours=remaining_hours)
    return adjusted_date

# Apply the adjustment to the 'Start' and 'End' columns
reference_date = pd.Timestamp('2024-08-01')
df['Start'] = df['Start'].apply(lambda x: adjust_for_working_days(reference_date, x.total_seconds() / 3600))
df['End'] = df['End'].apply(lambda x: adjust_for_working_days(reference_date, x.total_seconds() / 3600))

# Create Gantt chart using Plotly Express
fig = px.timeline(df, x_start="Start", x_end="End", y="Station", color="Hull", title="Operation Timeline")

# Show the plot
fig.show()