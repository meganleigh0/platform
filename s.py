import plotly.graph_objects as go
import pandas as pd

# Creating the data frame
data = {'Heads': [35, 36, 75],
        'Manpower': [280, 288, 600],
        'Actual Hours': [98, 121, 314],
        'Efficiency': [0.35, 0.42, 0.52]}
df = pd.DataFrame(data)

# Creating the plot
fig = go.Figure()

# Adding traces for each column
for col in df.columns:
    if col != 'Heads':
        fig.add_trace(go.Scatter(x=df['Heads'], y=df[col], mode='markers+lines', name=col))

# Updating layout for better visualization
fig.update_layout(title='Work Data Visualization',
                  xaxis_title='Heads',
                  yaxis_title='Values',
                  legend_title='Metrics',
                  yaxis=dict(tickformat='.2f'))

# Showing the plot
fig.show()