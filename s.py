
    # Create a list of heads required for used departments
    heads_required = [np.ceil(np.mean([h / 160 for h in sim_results[dep]])) if dep in sim_results else 0 for dep in df_department_data['DepID']]

    # Create a list of heads available for used departments
    heads_available = df_department_data[df_department_data['DepID'].isin(used_departments)]['Heads'].tolist()

    # Create a gauge chart based on heads comparison
    fig_gauge = go.Figure()

    # Add a bullet chart trace for the gauge
    fig_gauge.add_trace(go.Indicator(
        mode="number+gauge+delta",
        value=sum(heads_required),
        delta={'reference': sum(heads_available)},
        domain={'x': [0, 1], 'y': [0.2, 0.8]},
        title={'text': "Heads Required vs Available"},
        gauge={
            'axis': {'range': [0, max(sum(heads_available), sum(heads_required))]},
            'bar': {'color': "lightgray"},
            'steps': [
                {'range': [0, sum(heads_available)], 'color': "green"},
                {'range': [sum(heads_available), sum(heads_required)], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.75,
                'value': sum(heads_available)
            }
        }
    ))

    st.plotly_chart(fig_gauge)
