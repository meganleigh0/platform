import streamlit as st
import pandas as pd
from calendar import month_name

# Read the data from CSV files
station_data = pd.read_csv('station_requirements.csv')
department_data = pd.read_csv('department_requirements.csv')

# Convert 'Month' to datetime for proper sorting
station_data['Month'] = pd.to_datetime(station_data['Month'], format='%B %Y')
department_data['Month'] = pd.to_datetime(department_data['Month'], format='%B %Y')

# Layout style
st.set_page_config(layout="wide")

# Streamlit layout
st.title("Production Schedule Analysis")

# Month and Program Selection
sorted_months = sorted(station_data['Month'].unique())
sorted_month_names = [month_name[month.month] for month in sorted_months]
selected_month = st.sidebar.selectbox("Select a Month", sorted_month_names)
selected_month_datetime = next((month for month in sorted_months if month_name[month.month] == selected_month))

selected_program = st.sidebar.selectbox("Select a Program", ['All Programs'] + list(station_data['Program'].unique()))

# Filter data based on the selected month and program
if selected_program != 'All Programs':
    filtered_station_data = station_data[(station_data['Month'] == selected_month_datetime) & (station_data['Program'] == selected_program)]
    filtered_department_data = department_data[(department_data['Month'] == selected_month_datetime) & (department_data['Program'] == selected_program)]
else:
    filtered_station_data = station_data[station_data['Month'] == selected_month_datetime]
    filtered_department_data = department_data[department_data['Month'] == selected_month_datetime]

# Calculate total hours
total_vehicle_hours = filtered_station_data['Station Hours'].sum() + filtered_department_data['Department Hours'].sum()
program_quantity = filtered_station_data['Quantity'].iloc[0] if not filtered_station_data.empty else 1
total_program_hours = total_vehicle_hours * program_quantity

# Display total hours
col1, col2 = st.columns(2)
col1.metric("Total Vehicle Hours", total_vehicle_hours)
col2.metric("Total Program Hours", total_program_hours)

# Visualizations
st.header(f"Station and Department Hours for {selected_month}")
col3, col4 = st.columns(2)
with col3:
    st.subheader("Station Hours")
    station_chart = filtered_station_data.groupby('Station Name')['Station Hours'].sum().sort_values()
    st.bar_chart(station_chart)

with col4:
    st.subheader("Department Hours")
    department_chart = filtered_department_data.groupby('Department ID')['Department Hours'].sum().sort_values()
    st.bar_chart(department_chart)

# Detailed Data Tables (if required)
if st.checkbox("Show Detailed Data"):
    st.subheader("Detailed Station Data")
    st.dataframe(filtered_station_data)
    st.subheader("Detailed Department Data")
    st.dataframe(filtered_department_data)
