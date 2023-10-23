import pandas as pd
import plotly.express as px


# Create the line plot
fig = px.line(df, x='Time', y='ID', color='Vehicle', 
              line_shape='linear', title='Assembly Interactions over Time')

# Add scatter points on top of the lines
scatter = px.scatter(df, x='Time', y='ID', color='Vehicle')
for trace in scatter.data:
    fig.add_trace(trace)

# Show the figure
fig.show()