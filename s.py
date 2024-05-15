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

# Adding traces for each metric with separate y-axes
fig.add_trace(go.Scatter(x=df.index, y=df['Heads'], mode='lines+markers', name='Heads', yaxis='y1'))
fig.add_trace(go.Scatter(x=df.index, y=df['Manpower'], mode='lines+markers', name='Manpower', yaxis='y2'))
fig.add_trace(go.Scatter(x=df.index, y=df['Actual Hours'], mode='lines+markers', name='Actual Hours', yaxis='y3'))
fig.add_trace(go.Scatter(x=df.index, y=df['Efficiency'], mode='lines+markers', name='Efficiency', yaxis='y4'))

# Updating layout for better visualization
fig.update_layout(title='Work Data by Day',
                  xaxis_title='Day',
                  yaxis=dict(title='Heads', side='left', overlaying=False),
                  yaxis2=dict(title='Manpower', side='left', overlaying='y', anchor='free', position=0.05),
                  yaxis3=dict(title='Actual Hours', side='right', overlaying=False, anchor='free', position=0.95),
                  yaxis4=dict(title='Efficiency', side='right', overlaying='y', anchor='free', position=0.95),
                  legend_title='Metrics')

# Showing the plot
fig.show()