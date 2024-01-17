# Run Monte Carlo Simulations
if st.button('Run Simulations'):
    progress_bar = st.progress(0)  # Progress bar initialization
    sim_results = {dep: [] for dep in df_department_data['DepID']}
    for i in range(simulations):
        sim_reqs = calc_dep_requirements(selected_month, std)
        for dep, hours in sim_reqs.items():
            sim_results[dep].append(hours)
        progress_bar.progress((i + 1) / simulations)

    # Visualization for each department
    for dep, hours in sim_results.items():
        department_info = df_department_data[df_department_data['DepID'] == dep].iloc[0]
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=hours, name='Hours', marker_color='#FFA07A', opacity=0.6))
        fig.update_layout(title_text=f"Hours Distribution for {department_info['Name']}")
        st.plotly_chart(fig)

    # Calculate and Display Average Heads Required
    st.markdown("### Average Heads Required by Department")
    for dep in df_department_data['DepID']:
        avg_heads = np.mean([np.ceil(h / 160) for h in sim_results[dep]])
        shortage = avg_heads > df_department_data[df_department_data['DepID'] == dep]['Heads'].iloc[0]
        color = "red" if shortage else "green"
        st.markdown(f"**{dep} ({df_department_data[df_department_data['DepID'] == dep]['Name'].iloc[0]}):** {avg_heads} heads required", unsafe_allow_html=True)
        st.markdown(f"<span style='color: {color};'>{'Shortage' if shortage else 'Sufficient'}</span>", unsafe_allow_html=True)
