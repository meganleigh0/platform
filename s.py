import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import holidays

# Assume operation_df is your DataFrame
df = operation_df.copy()

# Convert the time columns to float if they are not already
df['Start'] = df['Start'].astype(float)
df['End'] = df['End'].astype(float)

# Define US holidays
us_holidays = holidays.US()

def adjust_for_working_days(start_date, timedelta_hours):
    remaining_hours = timedelta(hours=timedelta_hours).total_seconds() / 3600
    current_date = start_date

    while remaining_hours > 0:
        # Check if the current date is a working day
        if current_date.weekday() < 5 and current_date.date() not in us_holidays:
            # Calculate available hours in the current workday
            workday_end = current_date.replace(hour=17, minute=0, second=0, microsecond=0)
            workday_start = current_date.replace(hour=9, minute=0, second=0, microsecond=0)

            if current_date < workday_start:
                current_date = workday_start

            available_hours_today = (workday_end - current_date).total_seconds() / 3600

            if remaining_hours <= available_hours_today:
                current_date += timedelta(hours=remaining_hours)
                remaining_hours = 0
            else:
                remaining_hours -= available_hours_today
                current_date = workday_end + timedelta(days=1)
                current_date = current_date.replace(hour=9, minute=0, second=0, microsecond=0)
        else:
            # Move to the next day if it's a weekend or holiday
            current_date += timedelta(days=1)
            current_date = current_date.replace(hour=9, minute=0, second=0, microsecond=0)

    return current_date

# Apply the adjustment to the 'Start' and 'End' columns
reference_date = datetime(2024, 8, 1, 9)  # Assuming work starts at 9 AM on the reference date
df['Start'] = df['Start'].apply(lambda x: adjust_for_working_days(reference_date, x.total_seconds() / 3600))
df['End'] = df['End'].apply(lambda x: adjust_for_working_days(reference_date, x.total_seconds() / 3600))

# Create Gantt chart using Plotly Express
fig = px.timeline(df, x_start="Start", x_end="End", y="Station", color="Hull", title="Operation Timeline")

# Show the​⬤