 # Gauge chart for overall heads vs heads required
    fig_gauge = go.Figure(go.Indicator(
        mode = "number+gauge+delta",
        value = total_heads_required,
        delta = {'reference': total_heads},
        gauge = {'axis': {'range': [None, max(total_heads, total_heads_required)]},
                 'steps' : [{'range': [0, total_heads], 'color': "lightgreen"},
                            {'range': [total_heads, total_heads_required], 'color': "red"}],
                 'threshold' : {'line': {'color': "blue", 'width': 4}, 'thickness': 0.75, 'value': total_heads}}))

    fig_gauge.update_layout(title = 'Comparison of Total Heads Available vs Heads Required')
    st.plotly_chart(fig_gauge)
