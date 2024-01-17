  # Create a list of heads required for used departments
    heads_required = [np.ceil(np.mean([h / 160 for h in sim_results[dep]])) if dep in sim_results else 0 for dep in df_department_data['DepID']]

    # Create a list of heads available for used departments
    heads_available = df_department_data[df_department_data['DepID'].isin(used_departments)]['Heads'].tolist()

    # Create a gauge chart based on heads comparison
    fig_gauge = ff.create_bullet(
        orientation="h",
        titles=["Heads Required vs Available"],
        markers=total_heads_required,
        measures=heads_available,
        ranges=[total_heads_available],
        width=400,
        height=100
    )

    st.plotly_chart(fig_gauge)
