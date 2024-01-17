# UI Elements
st.title("Department Dashboard")

# Display initial Department Information Table
st.markdown("### Initial Department Information")
st.dataframe(df_department_data.style.set_properties(**{
    'background-color': '#f4f4f2',
    'color': '#0a3d62',
    'border-color': 'white',
    'text-align': 'center'
}))

# Input widgets for simulations
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
            if hours:  # Only consider non-empty values
                sim_results[dep].extend(hours)
        progress_bar.progress((i + 1) / simulations)

    # Plant aggregation for used departments
    st.markdown("### Heads Required by Plant")
    used_departments = {dep: res for dep, res in sim_results.items() if res}  # Filter out unused departments
    plant_needs = df_department_data[df_department_data['DepID'].isin(used_departments)].copy()
    plant_needs['Heads Required'] = plant_needs['DepID'].apply(lambda x: np.ceil(np.mean([h / 160 for h in sim_results[x]])) if x in sim_results else 0)
    plant_summary = plant_needs.groupby('Plant').agg({'Heads': 'sum', 'Heads Required': 'sum'}).reset_index()

    # Visualize plant needs
    fig = go.Figure(data=[
        go.Bar(name='Heads', x=plant_summary['Plant'], y=plant_summary['Heads']),
        go.Bar(name='Heads Required', x=plant_summary['Plant'], y=plant_summary['Heads Required'])
    ])
    fig.update_layout(barmode='group', title="Heads vs Heads Required by Plant")
    st.plotly_chart(fig)

    # Visualization and Summary for each used department
    st.markdown("### Department-wise Details")
    for dep, hours in used_departments.items():
        department_info = df_department_data[df_department_data['DepID'] == dep].iloc[0]
        avg_heads_required = np.mean([np.ceil(h / 160) for h in hours])
        fig = go.Figure(data=[
            go.Histogram(x=hours, name='Hours', marker_color='#FFA07A', opacity=0.6)
        ])
        fig.update_layout(title_text=f"Hours Distribution for {department_info['Name']}")
        st.plotly_chart(fig)

        shortage = avg_heads_required > department_info['Heads']
        color = "red" if shortage else "green"
        st.markdown(f"**{department_info['Name']} (DepID: {dep}):** {int(avg_heads_required)} heads required", unsafe_allow_html=True)
        st.markdown(f"<span style='color: {color};'>{'Shortage' if shortage else 'Sufficient'}</span>", unsafe_allow_html=True)
