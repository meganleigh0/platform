import plotly.graph_objects as go
import pandas as pd

# Example DataFrame
data = {
    'station': ['Station A', 'Station B', 'Station C', 'Station D'],
    'assembly_count': [100, 150, 200, 120],
    'operation_count': [80, 160, 140, 130],
    'departments': ['Dept 1', 'Dept 2', 'Dept 3', 'Dept 1']
}
df = pd.DataFrame(data)

# Bar Chart for Assembly and Operation Counts by Station
fig = go.Figure(data=[
    go.Bar(name='Assembly Count', x=df['station'], y=df['assembly_count'], marker_color='indianred'),
    go.Bar(name='Operation Count', x=df['station'], y=df['operation_count'], marker_color='lightsalmon')
])

# Update the layout
fig.update_layout(barmode='group', title_text='Assembly and Operation Counts by Station')
fig.show()

# Bubble Chart for Assembly and Operation Count by Department
fig = go.Figure(data=[go.Scatter(
    x=df['assembly_count'],
    y=df['operation_count'],
    text=df['departments'],
    mode='markers',
    marker=dict(
        size=df['operation_count'],
        color=df['departments'].astype('category').cat.codes, # Assign a unique color to each department
        showscale=True
    )
)])

fig.update_layout(title_text='Assembly vs. Operation Count by Department', xaxis_title='Assembly Count', yaxis_title='Operation Count')
fig.show()

# Pie Chart for Department Distribution
dept_counts = df['departments'].value_counts()
fig = go.Figure(data=[go.Pie(labels=dept_counts.index, values=dept_counts.values)])

fig.update_layout(title_text='Department Distribution Across Stations')
fig.show()