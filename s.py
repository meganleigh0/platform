import plotly.graph_objects as go
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Creating the data frame
data = {'Heads': [35, 36, 75],
        'Manpower': [280, 288, 600],
        'Actual Hours': [98, 121, 314],
        'Efficiency': [0.35, 0.42, 0.52]}
df = pd.DataFrame(data)

# Normalize the data
scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(df)

# Creating the plot
fig = go.Figure()

# Adding traces for each metric
fig.add_trace(go.Bar(x=df.index, y=normalized_data[:, 0], name='Heads'))
fig.add_trace(go.Bar(x=df.index, y=normalized_data[:, 1], name='Manpower'))
fig.add_trace(go.Bar(x=df.index, y=normalized_data[:, 2], name='Actual Hours'))
fig.add_trace(go.Bar(x=df.index, y=normalized_data[:, 3], name='Efficiency'))

# Updating layout for better visualization
fig.update_layout(barmode='group',
                  title='Normalized Work Data by Day',
                  xaxis_title='Day',
                  yaxis_title='Normalized Values',
                  legend_title='Metrics')

# Showing the plot
fig.show()