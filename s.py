import streamlit as st
import pandas as pd
from datetime import datetime

# Assuming dataframes are loaded here
# station_requirements = pd.DataFrame([...])
# department_requirements = pd.DataFrame([...])
# schedule = pd.DataFrame([...])

# Helper function to get month number
def month_to_number(month_name):
    datetime_object = datetime.strptime(month_name, "%B %Y")
    return datetime_object.month

# Modified function to sort months
def sort_months(months):
    return sorted(months, key=month_to_number)

# Modified calculate_hours function
def calculate_hours(requirements_df, schedule_df, selected_month=None, selected_program=None):
    filtered_schedule = schedule_df.copy()

    if selected_month:
        filtered_schedule = filtered_schedule[['Program', selected_month]]
    else:
        filtered_schedule = filtered_schedule[['Program'] + sort_months(list(schedule_df.columns[2:]))]

    if selected_program and selected_program != 'All Programs':
        filtered_schedule = filtered_schedule[filtered_schedule['Program'] == selected_program]

    merged_df = pd.merge(filtered_schedule, requirements_df, on='Program')
    total_hours_program = 0
    total_hours_vehicle = 0

    if selected_month:
        merged_df['Total Hours'] = merged_df[selected_month] * merged_df['Hours']
        total_hours_program = merged_df['Total Hours'].sum()
        if not merged_df[selected_month].empty:
            total_hours_vehicle = merged_df[selected_month].mean() * merged_df['Hours'].mean()
    else:
        for month in sort_months(list(schedule_df.columns[2:])):
            merged_df[month] = merged_df[month] * merged_df['Hours']
            total_hours_program += merged_df[month].sum()

    return merged_df, total_hours_vehicle, total_hours_program

# Streamlit layout and rest of your code remains the same
