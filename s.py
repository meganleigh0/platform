# Create a custom layout with shapes for curved bars
    layout = {
        'shapes': [
            {
                'type': 'path',
                'path': f'M {0.15 * np.pi} {0.5} L {-0.15 * np.pi} {0.5} L {0.15 * np.pi} {0.3} Z',
                'fillcolor': gauge_color,
                'line': {'color': gauge_color}
            },
            {
                'type': 'path',
                'path': f'M {0.85 * np.pi} {0.5} L {1.15 * np.pi} {0.5} L {0.85 * np.pi} {0.3} Z',
                'fillcolor': 'lightgray',
                'line': {'color': 'lightgray'}
            }
        ],
        'xaxis': {'showticklabels': False, 'showgrid': False, 'zeroline': False},
        'yaxis': {'showticklabels': False, 'showgrid': False, 'zeroline': False},
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    }

    fig_gauge = go.Figure(go.Indicator(
        mode = "number+delta",
        value = total_heads_required,
        delta = {'reference': total_heads_used_departments},
        gauge = {'shape': 'angular'},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))

    fig_gauge.update_layout(layout)
    fig_gauge.update_layout(title = 'Comparison of Total Heads Available vs Heads Required (Used Departments)')
    st.plotly_chart(fig_gauge)
