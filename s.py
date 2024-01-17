    # Gauge chart for overall heads vs heads required (based on used departments)
    total_heads_used_departments = plant_needs['Heads'].sum()
    total_heads_required = plant_needs['Heads Required'].sum()

    fig_gauge = go.Figure(go.Indicator(
        mode = "number+delta",
        value = total_heads_required,
        delta = {'reference': total_heads_used_departments, 'increasing': {'color': "Red"}, 'decreasing': {'color': "Green"}},
        gauge = {'axis': {'range': [None, max(total_heads_used_departments, total_heads_required)]},
                 'steps' : [{'range': [0, total_heads_used_departments], 'color': "lightgray"}],
                 'threshold' : {'line': {'color': "blue", 'width': 4}, 'thickness': 0.75, 'value': total_heads_used_departments}})
    )

    fig_gauge.update_layout(title = 'Comparison of Total Heads Available vs Heads Required (Used Departments)')
    st.plotly_chart(fig_gauge)
