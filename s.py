import streamlit as st
import pandas as pd

# Assuming dataframes are loaded here
# station_requirements = pd.DataFrame([...])
# department_requirements = pd.DataFrame([...])
# schedule = pd.DataFrame([...])

# Function to calculate hours
def calculate_hours(requirements_df, schedule_df, selected_month=None, selected_program=None):
    filtered_schedule = schedule_df.copy()

    if selected_month:
        filtered_schedule = filtered_schedule[['Program', selected_month]]
    else:
        filtered_schedule = filtered_schedule[['Program'] + list(schedule_df.columns[2:])]

    if selected_program and selected_program != 'All Programs':
        filtered_schedule = filtered_schedule[filtered_schedule['Program'] == selected_program]

    merged_df = pd.merge(filtered_schedule, requirements_df, on='Program')
    if selected_month:
        merged_df['Total Hours'] = merged_df[selected_month] * merged_df['Hours']
    else:
        for month in schedule_df.columns[2:]:
            merged_df[month] = merged_df[month] * merged_df['Hours']

    return merged_df

# Streamlit layout
st.set_page_config(layout="wide")
st.title("Production Schedule Analysis")

# Selection options
months = ['All Months'] + list(schedule.columns[2:])
programs = ['All Programs'] + list(schedule['Program'].unique())
selected_month = st.selectbox("Select a Month", months)
selected_program = st.selectbox("Select a Program", programs)

# Calculate hours for station and department
station_hours = calculate_hours(station_requirements, schedule, selected_month if selected_month != 'All Months' else None, selected_program)
department_hours = calculate_hours(department_requirements, schedule, selected_month if selected_month != 'All Months' else None, selected_program)

# Display the schedule for context
st.header("Production Schedule")
st.dataframe(schedule)

# Display results
st.header("Station and Department Hours")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Station Hours")
    if selected_month != 'All Months':
        st.bar_chart(station_hours.groupby('Station')['Total Hours'].sum())
    else:
        st.line_chart(station_hours.groupby('Station')[schedule.columns[2:]].sum())

with col2:
    st.subheader("Department Hours")
    if selected_month != 'All Months':
        st.bar_chart(department_hours.groupby('DepartmentID')['Total Hours'].sum())
    else:
        st.line_chart(department_hours.groupby('DepartmentID')[schedule.columns[2:]].sum())
