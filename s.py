import plotly.graph_objects as go
import plotly.express as px

# Assuming df2 is already created with 'ActionCategory', 'Hours', and 'Count'

# Create a bar chart for the count of action categories
bar_chart = go.Figure()

bar_chart.add_trace(go.Bar(
    x=df2['ActionCategory'], 
    y=df2['Count'],
    text=df2['Count'], 
    textposition='outside', 
    marker=dict(color='lightblue'),
    name="Action Category Count"
))

# Remove grid, spines, and ticks to create a minimalist chart
bar_chart.update_layout(
    title="Action Category Count",
    showlegend=False,
    xaxis_title="Action Category",
    yaxis_title="Count",
    xaxis=dict(showline=False, showgrid=False, zeroline=False),
    yaxis=dict(showline=False, showgrid=False, zeroline=False),
    plot_bgcolor='white',
    height=400,
    width=600,
    margin=dict(l=0, r=0, t=30, b=30)
)

# Add hover labels for direct data display
bar_chart.update_traces(
    hovertemplate="Category: %{x}<br>Count: %{y}",
    marker_line_width=1.5
)

# Create a pie chart for total hours, styled minimally like a doughnut
pie_chart = go.Figure()

pie_chart.add_trace(go.Pie(
    labels=df2['ActionCategory'],
    values=df2['Hours'],
    hole=.4,  # To simulate a doughnut chart
    textinfo='label+percent',
    hoverinfo='label+value',
    marker=dict(line=dict(color='#000000', width=1.5))
))

# Style the pie chart to be minimalist
pie_chart.update_layout(
    title="Total Hours by Action Category",
    showlegend=False,
    height=400,
    width=600,
    margin=dict(l=0, r=0, t=30, b=30)
)

# Show both graphs side by side
bar_chart.show()
pie_chart.show()