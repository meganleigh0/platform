bar_chart = go.Figure(data=[go.Bar(x=station_count['Station'], y=station_count['Assembly Count'])])
bar_chart.update_layout(
    xaxis_title="Station",
    yaxis_title="Assembly Count",
    showlegend=False  # This should ensure no legend is displayed
)
