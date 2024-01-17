# Gauge chart for overall heads vs heads required (based on used departments)
    total_heads_used_departments = plant_needs['Heads'].sum()
    total_heads_required = plant_needs['Heads Required'].sum()

    # Determine gauge color based on heads comparison
    if total_heads_required > total_heads_used_departments:
        gauge_color = "Red"  # Shortfall
    elif total_heads_required < total_heads_used_departments:
        gauge_color = "Green"  # Surplus
    else:
        gauge_color = "Yellow"  # Exact match

    fig_gauge = go.Figure(go.Indicator(
        mode = "number+delta",
        value = total_heads_required,
        delta = {'reference': total_heads_used_departments},
        gauge = {'axis': {'range': [None, max(total_heads_used_departments, total_heads_required)]},
                 'bar': {'color': gauge_color},
                 'steps' : [{'range': [0, total_heads_used_departments], 'color': "lightgray"}],
                 'threshold' : {'line': {'color': "blue", 'width': 4}, 'thickness': 0.75, 'value': total_heads_used_departments}})
    )

    fig_gauge.update_layout(title = 'Comparison of Total Heads Available vs Heads Required (Used Departments)')
    st.plotly_chart(fig_gauge)
