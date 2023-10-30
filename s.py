import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Sample dataframe
data = {'AssemblyID': [1, 2, 1, 2, 1, 2, 1, 2],
        'Interaction': ['start', 'start', 'end', 'end', 'start', 'start', 'end', 'end'],
        'Station': ['station 1', 'station 2', 'station 1', 'station 2', 'station 1', 'station 2', 'station 1', 'station 2'],
        'Timestamp': [0.000, 0.000, 2.000, 3.000, 3.000, 5.000, 8.000, 9.000],
        'Vehicle': [1, 1, 1, 1, 2, 2, 2, 2]}

df = pd.DataFrame(data)
stations = df['Station'].unique()
num_stations = len(stations)

# Set up the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=10*60*1000,  # 10 minutes in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('live-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    time_passed = n * 10  # 10 minutes per interval
    ongoing_df = df[df['Timestamp'] <= time_passed]
    
    traces = []
    for _, row in ongoing_df.iterrows():
        y = list(stations).index(row['Station'])
        if row['Interaction'] == 'start':
            color = 'green'
        else:
            color = 'red'
        trace = go.Scatter(x=[row['Timestamp']], y=[y],
                           mode='markers',
                           marker=dict(color=color),
                           name=f"Vehicle {row['Vehicle']}")
        traces.append(trace)
    
    layout = go.Layout(title='Vehicles Moving Through Stations',
                       xaxis=dict(title='Time (hours)'),
                       yaxis=dict(tickvals=list(range(num_stations)),
                                  ticktext=stations, title='Stations'),
                       showlegend=False)
    
    return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)