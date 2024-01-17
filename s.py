    fig_gauge = go.Figure(go.Indicator(
        mode = "number+delta",
        value = total_heads_required,
        delta = {'reference': total_heads_used_departments},
        gauge = {'shape': 'angular'},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f'Total Heads Required vs Available ({gauge_color})'},
        gauge_axis = {
            'axis': {'range': [0, max(total_heads_used_departments, total_heads_required)]},
            'bar': {'color': gauge_color},
            'steps' : [{'range': [0, total_heads_used_departments], 'color': "lightgray"}],
            'threshold' : {'line': {'color': "blue", 'width': 4}, 'thickness': 0.75, 'value': total_heads_used_departments}
        }
    ))

    st.plotly_chart(fig_gauge)
