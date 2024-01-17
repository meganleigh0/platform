import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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
department_table.dataframe(df_department_data.style.set_properties(**{'background-color': 'black', 
                                                                     'color': 'lawngreen', 
                                                                     'border-color': 'white'}))

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
        lambda dep: np.mean([np.ceil(h / 160) for h in sim_results[dep]]) if dep in sim_results else None
    )

    # Style the DataFrame
    def highlight_red(val):
        color = 'red' if val > df_department_data.loc[df_department_data['DepID'] == val.name, 'Heads'].iloc[0] else 'lawngreen'
        return f'color: {color}'

    styled_df = df_department_data.style.applymap(highlight_red, subset=['Average Heads Required'])
    styled_df = styled_df.set_properties(**{'background-color': 'black', 'border-color': 'white'})

    # Update the table with the new data
    department_table.dataframe(styled_df)
