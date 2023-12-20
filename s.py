import streamlit as st
import pandas as pd

# Read the data from CSV files
station_data = pd.read_csv('station_requirements.csv')
department_data = pd.read_csv('department_requirements.csv')

# Layout style
st.set_page_config(layout="wide")

# Streamlit layout
st.title("Production Schedule Analysis")

# Month and Program Selection
selected_month = st.sidebar.selectbox("Select a Month", sorted(station_data['Month'].unique()))
selected_program = st.sidebar.selectbox("Select a Program", ['All Programs'] + list(station_data['Program'].unique()))

# Filter data based on the selected month and program
if selected_program != 'All Programs':
    station_data = station_data[(station_data['Month'] == selected_month) & (station_data['Program'] == selected_program)]
    department_data = department_data[(department_data['Month'] == selected_month) & (department_data['Program'] == selected_program)]
else:
    station_data = station_data[station_data['Month'] == selected_month]
    department_data = department_data[department_data['Month'] == selected_month]

# Calculate total hours
total_station_hours = station_data['Station Hours'].sum()
total_department_hours = department_data['Department Hours'].sum()

# Display total hours
col1, col2 = st.columns(2)
col1.metric("Total Station Hours", total_station_hours)
col2.metric("Total Department Hours", total_department_hours)

# Visualizations
st.header(f"Station and Department Hours for {selected_month}")
col3, col4 = st.columns(2)
with col3:
    st.subheader("Station Hours")
    station_chart = station_data.groupby('Station Name')['Station Hours'].sum().sort_values()
    st.bar_chart(station_chart)

with col4:
    st.subheader("Department Hours")
    department_chart = department_data.groupby('Department ID')['Department Hours'].sum().sort_values()
    st.bar_chart(department_chart)

# Detailed Data Tables (if required)
if st.checkbox("Show Detailed Data"):
    st.subheader("Detailed Station Data")
    st.dataframe(station_data)
    st.subheader("Detailed Department Data")
    st.dataframe(department_data)
