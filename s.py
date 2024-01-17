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
    'Name': ['Manufacturing', 'Design'],
    'Heads': [10, 12],
    'Plant': ['A', 'B'],
    'Efficiency': [0.8, 0.7]
})

# UI Elements
st.title("Department Dashboard")

# Display Department Information Table
st.markdown("### Department Information")
st.dataframe(df_department_data.style.set_properties(**{
    'background-color': '#f4f4f2',
    'color': '#0a3d62',
    'border-color': 'white',
    'text-align': 'center'
}))

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
    df_department_data['Heads Required'] = df_department_data['DepID'].apply(
        lambda dep: np.mean([np.ceil(h / 160) for h in sim_results[dep]]) if dep in sim_results else 0
    )

    # Aggregate heads by plant
    plant_agg = df_department_data.groupby('Plant').agg({'Heads': 'sum', 'Heads Required': 'sum'}).reset_index()
    
    # Visualization and Summary
    for dep, hours in sim_results.items():
        department_info = df_department_data[df_department_data['DepID'] == dep].iloc[0]
        # Overlay Histograms for Hours and Head Count
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=hours, name='Hours', opacity=0.6))
        fig.add_trace(go.Histogram(x=[np.ceil(h / 160) for h in hours], name='Head Count', opacity=0.6))
        fig.update_layout(title_text=f"Distributions for {department_info['Name']}", barmode='overlay')
        st.plotly_chart(fig)

    # Display Updated Department Table
    st.markdown("### Updated Department Information")
    st.dataframe(df_department_data.style.apply(lambda x: ['background-color: red' if x['Heads Required'] > x['Heads'] else 'background-color: green' for _ in x], axis=1))

    # Display Plant Aggregation Table
    st.markdown("### Plant-wise Heads Requirement")
    st.dataframe(plant_agg.style.apply(lambda x: ['background-color: red' if x['Heads Required'] > x['Heads'] else 'background-color: green' for _ in x], axis=1))
