import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Dummy function for calc_dep_requirements
# Replace this with your actual function
def calc_dep_requirements(month, std):
    # This should return a dictionary with department requirements based on the month and std
    return {'dept1': np.random.normal(120, std), 'dept2': np.random.normal(150, std)}  # example return value

# Dummy DataFrame for department data
# Replace this with your actual DataFrame
df_department_data = pd.DataFrame({
    'DepID': ['dept1', 'dept2'],
    'Heads': [10, 12],
    'Efficiency': [0.8, 0.7],
    'Name': ['Manufacturing', 'Design']
})

# UI Elements
st.title("Department Dashboard")

list_of_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
selected_month = st.selectbox('Select Month', list_of_months)
std = st.number_input('Enter Standard Deviation', min_value=0.0, value=1.0)
simulations = st.number_input('Enter Number of Simulations', min_value=1, value=100)

# Run Monte Carlo Simulations
if st.button('Run Simulations'):
    sim_results = {dep: [] for dep in df_department_data['DepID']}

    for _ in range(simulations):
        sim_reqs = calc_dep_requirements(selected_month, std)
        for dep, hours in sim_reqs.items():
            sim_results[dep].append(hours)

    # Visualization
    for dep, hours in sim_results.items():
        department_name = df_department_data[df_department_data['DepID'] == dep]['Name'].iloc[0]
        fig = px.histogram(hours, title=f"Hours Distribution for {department_name}", labels={'value': 'Hours'}, nbins=30)
        st.plotly_chart(fig)

        # Calculating Head Count from Hours
        head_counts = [np.ceil(h / 160) for h in hours]
        fig_head_count = px.histogram(head_counts, title=f"Head Count Distribution for {department_name}", labels={'value': 'Head Count'}, nbins=30)
        st.plotly_chart(fig_head_count)