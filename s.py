import streamlit as st
import pandas as pd

# Assuming dataframes are loaded here
# station_requirements = pd.DataFrame([...])
# department_requirements = pd.DataFrame([...])
# schedule = pd.DataFrame([...])

# Function to calculate hours for a given month
def calculate_monthly_hours(schedule_df, requirements_df, selected_month):
    # Filter schedule for the selected month and merge with requirements
    month_schedule = schedule_df[['Program', selected_month]]
    merged_df = pd.merge(month_schedule, requirements_df, on='Program')

    # Calculate total hours for the month
    merged_df['Total Hours'] = merged_df[selected_month] * merged_df['Hours']
    return merged_df.groupby(['Station' if 'Station' in requirements_df.columns else 'DepartmentID'])['Total Hours'].sum()

# Streamlit layout
st.set_page_config(layout="wide")
st.title("Production Schedule Analysis")

# Month selection
selected_month = st.selectbox("Select a Month", schedule.columns[2:])

# Calculate hours for station and department
station_hours = calculate_monthly_hours(schedule, station_requirements, selected_month)
department_hours = calculate_monthly_hours(schedule, department_requirements, selected_month)

# Display results
col1, col2 = st.columns(2)
with col1:
    st.header(f"Station Hours for {selected_month}")
    st.bar_chart(station_hours)

with col2:
    st.header(f"Department Hours for {selected_month}")
    st.bar_chart(department_hours)
