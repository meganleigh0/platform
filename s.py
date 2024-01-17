import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Dummy function for calc_dep_requirements
# Replace this with your actual function
def calc_dep_requirements(month, std):
    # Example return value, replace with actual logic
    return {'dept1': np.random.normal(120, std), 'dept2': np.random.normal(150, std), 'dept3': None}

# Dummy DataFrame for department data
# Replace this with your actual DataFrame
df_department_data = pd.DataFrame({
    'DepID': ['dept1', 'dept2', 'dept3'],
    'Heads': [10, 12, 15],
    'Efficiency': [0.8, 0.7, 0.6],
    'Name': ['Manufacturing', 'Design', 'Logistics']
})

# UI Elements
st.title("Department Dashboard")

# Styling for tables
def stylish(df):
    return df.style.set_properties(**{
        'background-color': '#f4f4f2',
        'color': '#0a3d62',
        'border-color': 'white',
        'text-align': 'center'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#f4f4f2'), ('color', '#0a3d62')]
    }])

# Display Department Information Table
st.markdown("### Department Information")
st.dataframe(stylish(df_department_data))

list_of_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
selected_month = st.selectbox('Select Month', list_of_months)
std = st.number_input('Enter Standard Deviation', min_value=0.0, value=1.0)
simulations = st.number_input('Enter Number of Simulations', min_value=1, value=100)

# Run Monte Carlo Simulations
if st.button('Run Simulations'):
    with st.spinner('Running simulations...'):
        sim_results = {dep: [] for dep in df_department_data['DepID'] if dep is not None}
        for i in range(simulations):
            sim_reqs = calc_dep_requirements(selected_month, std)
            for dep, hours in sim_reqs.items():
                if hours is not None:
                    sim_results[dep].append(hours)
            st.progress((i + 1) / simulations)

    # Visualization and Summary
    summary_data = []
    for dep, hours in sim_results.items():
        if hours:
            department_info = df_department_data[df_department_data['DepID'] == dep].iloc[0]
            avg_head_count = np.mean([np.ceil(h / 160) for h in hours])
            summary_data.append({
                'DepID': dep, 
                'Department Name': department_info['Name'], 
                'Average Head Count': avg_head_count,
                'Actual Efficiency': department_info['Efficiency'],
                'Actual Heads': department_info['Heads']
            })

            # Plotting histograms side by side
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=hours, name='Hours', marker_color='#FFA07A', nbinsx=30))
            fig.add_trace(go.Histogram(x=[np.ceil(h / 160) for h in hours], name='Head Count', marker_color='#20B2AA', nbinsx=30))
            fig.update_layout(title_text=f"Histograms for {department_info['Name']}", barmode='overlay')
            fig.update_traces(opacity=0.75)
            st.plotly_chart(fig)

    # Display Summary Table
    if summary_data:
        st.markdown("### Simulation Summary")
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(stylish(summary_df))
