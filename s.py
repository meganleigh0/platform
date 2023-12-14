import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Assuming the provided code, necessary libraries, and viz module are imported
simulation = Simulation()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Production Schedule Simulator"),
    dcc.Dropdown(
        id='month-selector',
        options=[
            {'label': month, 'value': month} for month in simulation.schedule.months
        ],
        value='January 2024'
    ),
    dcc.Input(id='rate-input', type='number', placeholder='Enter Rate'),
    dcc.RadioItems(
        id='duration-selector',
        options=[
            {'label': 'Day', 'value': 1},
            {'label': 'Week', 'value': 7},
            {'label': 'Month', 'value': 30}
        ],
        value=1
    ),
    html.Button('Run Simulation', id='run-simulation-btn'),
    dcc.Graph(id='gantt-chart')
])

@app.callback(
    Output('gantt-chart', 'figure'),
    [Input('run-simulation-btn', 'n_clicks')],
    [State('month-selector', 'value'),
     State('rate-input', 'value'),
     State('duration-selector', 'value')]
)
def update_gantt_chart(n_clicks, selected_month, rate, duration):
    if n_clicks:
        simulation.run_simulation(rate, duration, selected_month)
        logger.save_to_csv('assembly.csv')
        gantt_chart = viz.gantt()
        return gantt_chart
    return go.Figure()

if __name__ == '__main__':
    app.run_server(debug=True)
