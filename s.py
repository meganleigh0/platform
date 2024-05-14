import plotly.graph_objects as go
import pandas as pd

# Sample data creation (replace this with your actual dataframe)
data = {
    'Department1': [10, 15, 9, 7],
    'Department2': [12, 9, 7, 5],
    'Department3': [5, 3, 2, 4]
}
df = pd.DataFrame(data, index=pd.Index([1, 2, 3, 4], name='Day'))

# Create a figure with plotly
fig = go.Figure()

# Add a bar chart to the figure for each department
for department in df.columns:
    fig.add_trace(go.Bar(
        x=df.index,
        y=df[department],
        name=department
    ))

# Update layout for a stacked bar chart
fig.update_layout(
    barmode='stack',
    title='Manpower Loading Chart',
    xaxis_title='Day',
    yaxis_title='Hours',
    legend_title='Department'
)

# Show the figure
fig.show()