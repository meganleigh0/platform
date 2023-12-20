import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Example dataframes (replace with actual data)
# station_requirements = pd.DataFrame([...])
# department_requirements = pd.DataFrame([...])
# schedule = pd.DataFrame([...])

# Streamlit layout
st.set_page_config(layout="wide")
st.title("Production Schedule Analysis")

# Selection options
st.sidebar.header("Select Options")
selected_month = st.sidebar.selectbox("Select a Month", ['All'] + list(schedule.columns[2:]))
selected_program = st.sidebar.selectbox("Select a Program", ['All'] + list(schedule['Program'].unique()))

# Function to calculate requirements
def calculate_requirements(selected_month, selected_program):
    month_filter = (schedule.columns[2:] if selected_month == 'All' else [selected_month])
    program_filter = (schedule['Program'] if selected_program == 'All' else [selected_program])

    month_schedule = schedule[schedule['Program'].isin(program_filter)][['Program'] + month_filter]
    station_req = pd.merge(month_schedule, station_requirements, on='Program')
    department_req = pd.merge(month_schedule, department_requirements, on='Program')

    station_req['Total Station Hours'] = station_req[month_filter].multiply(station_req['Hours'], axis="index")
    department_req['Total Department Hours'] = department_req[month_filter].multiply(department_req['Hours'], axis="index")

    return station_req, department_req

station_req, department_req = calculate_requirements(selected_month, selected_program)

# Display total hours
col1, col2 = st.columns(2)
with col1:
    st.header("Total Station Hours")
    st.bar_chart(station_req.groupby('Program')['Total Station Hours'].sum())

with col2:
    st.header("Total Department Hours")
    st.bar_chart(department_req.groupby('Program')['Total Department Hours'].sum())

# Detailed Data Tables (if required)
if st.checkbox("Show Detailed Data", False):
    st.subheader("Detailed Station Data")
    st.dataframe(station_req)
    st.subheader("Detailed Department Data")
    st.dataframe(department_req)
