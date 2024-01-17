import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Dummy function for calc_dep_requirements
# Replace this with your actual function
def calc_dep_requirements(month, std):
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

# Display Department Information Table
st.markdown("### Department Information")
department_table = st.empty()  # Placeholder for the department table

# Initialize table styling
def style_table(df):
    return df.style.apply(lambda x: ['background: red' if v > x['Heads'] else 'background: green' for v in x['Average Heads Required']], axis=1)

# Input widgets
list_of_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
selected_month = st.selectbox('Select Month', list_of_months)
std = st.number_input('Enter Standard Deviation', min_value=0.0, value=1.0)
simulations = st.number_input('Enter Number of Simulations', min_value=1, value=100)

# Run Monte Carlo Simulations
if st.button('Run Simulations'):
    progress_bar = st.progress(0)  # Progress bar initialization
    sim_results = {dep: [] for dep in df_department_data['DepID']}
    for i in range(simulations):
        sim_reqs = calc_dep_requirements(selected_month, std)
        for dep, hours in sim_reqs.items():
            sim_results[dep].append(hours)
        progress_bar.progress((i + 1) / simulations)

    # Update Department Data with Simulation Results
    df_department_data['Average Heads Required'] = df_department_data['DepID'].apply(
        lambda dep: np.mean([np.ceil(h / 160) for h in sim_results[dep]]) if dep in sim_results else 0
    )

    # Visualization and Summary
    for dep, hours in sim_results.items():
        department_info = df_department_data[df_department_data['DepID'] == dep].iloc[0]
        # Overlay Histograms for Hours and Head Count
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=hours, name='Hours', opacity=0.6))
        fig.add_trace(go.Histogram(x=[np.ceil(h / 160) for h in hours], name='Head Count', opacity=0.6))
        fig.update_layout(title_text=f"Distributions for {department_info['Name']}", barmode='overlay')
        st.plotly_chart(fig)

    # Style and Display the Updated Department Table
    styled_df = style_table(df_department_data)
    department_table.dataframe(styled_df)
