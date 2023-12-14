import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

# Assuming the provided code and necessary libraries are imported
simulation = Simulation()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Production Schedule Simulator"),
    dcc.Dropdown(
        id='month-selector',
        options=[{'label': month, 'value': month} for month in simulation.schedule.months],
        value='January 2024'
    ),
    dcc.Input(id='rate-input', type='number', value=5, placeholder='Enter Rate'),
    dcc.RadioItems(
        id='duration-selector',
        options=[{'label': 'Day', 'value': 1}, {'label': 'Week', 'value': 7}, {'label': 'Month', 'value': 30}],
        value=1
    ),
    html.Button('Run Simulation', id='run-simulation-btn'),
    html.Div(id='schedule-table'),
    dcc.Graph(id='gantt-chart', figure=go.Figure())
])

@app.callback(
    Output('schedule-table', 'children'),
    [Input('run-simulation-btn', 'n_clicks')],
    [State('month-selector', 'value'),
     State('rate-input', 'value'),
     State('duration-selector', 'value')]
)
def update_schedule_table(n_clicks, selected_month, rate, duration):
    if n_clicks:
        print("Simulation started")  # Logging to console
        # Dummy data for testing
        return html.Table([html.Tr([html.Td("Simulation Data Here")])])
    return "Click 'Run Simulation' to display the schedule."

if __name__ == '__main__':
    app.run_server(debug=True)
