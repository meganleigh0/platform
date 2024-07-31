import pandas as pd
import plotly.express as px
from pandas.tseries.offsets import BDay
import holidays

# Assume operation_df is your DataFrame
df = operation_df.copy()

# Convert the time columns to float if they are not already
df['Start'] = df['Start'].astype(float)
df['End'] = df['End'].astype(float)

# Convert the time to a proper timedelta format
df['Start'] = pd.to_timedelta(df['Start'], unit='h')
df['End'] = pd.to_timedelta(df['End'], unit='h')

# Create a business day offset with US holidays
us_holidays = holidays.US()
custom_bday = BDay(holidays=us_holidays)

def adjust_for_working_days(start_date, timedelta_hours):
    total_days = timedelta(hours=timedelta_hours).days
    remaining_hours = timedelta(hours=timedelta_hours).seconds // 3600
    adjusted_date = start_date + total_days * custom_bday
    adjusted_date += pd.Timedelta(hours=remaining_hours)
    return adjusted_date

# Apply the adjustment to the 'Start' and 'End' columns
reference_date = pd.Timestamp('2024-08-01')
df['Start'] = df['Start'].apply(lambda x: adjust_for_working_days(reference_date, x.total_seconds() / 3600))
df['End'] = df['End'].apply(lambda x: adjust_for_working_days(reference_date, x.total_seconds() / 3600))

# Create Gantt chart using Plotly Express
fig = px.timeline(df, x_start="Start", x_end="End", y="Station", color="Hull", title="Operation Timeline")

# Show the plot
fig.show()