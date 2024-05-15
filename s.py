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

# Adding trace for Actual Hours vs. Day
fig.add_trace(go.Bar(x=df.index, y=df['Actual Hours'], name='Actual Hours'))

# Updating layout for better visualization
fig.update_layout(title='Utilization by Day',
                  xaxis_title='Day',
                  yaxis_title='Actual Hours',
                  legend_title='Metrics')

# Showing the plot
fig.show()