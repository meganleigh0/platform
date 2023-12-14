import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
import simpy  # Ensure simpy is installed

# Assuming the provided code and necessary libraries are imported

simulation = Simulation()  # Create a simulation instance

# Function to extract and format schedule data for DataTable
def generate_schedule_table(schedule):
    data = []
    for program_key, program_obj in schedule.programs.items():
        program_name = program_key[0]
        for month, quantity in program_obj.production_plan.items():
            data.append({'Program': program_name, 'Month': month, 'Quantity': quantity})
    
    return pd.DataFrame(data)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Production Schedule Simulator"), width={'size': 6, 'offset': 3})),
    dbc.Row(dbc.Col(dash_table.DataTable(id='schedule-table'), width=12)),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='month-selector',
            options=[{'label': month, 'value': month} for month in simulation.schedule.months],
            value='January 2024'), width=4),
        dbc.Col(dcc.RadioItems(
            id='duration-selector',
            options=[{'label': 'Day', 'value': 1}, {'label': 'Week', 'value': 7}, {'label': 'Month', 'value': 30}],
            value=1), width=4),
        dbc.Col(dbc.Button('Run Simulation', id='run-simulation-btn', color="primary"), width=2),
        dbc.Col(dbc.Button('Clear Simulation', id='clear-simulation-btn', color="secondary"), width=2)
    ]),
    dbc.Row(dbc.Col(dcc.Graph(id='gantt-chart', figure=go.Figure()), width=12))
], fluid=True)

@app.callback(
    [Output('gantt-chart', 'figure'),
     Output('schedule-table', 'data')],
    [Input('run-simulation-btn', 'n_clicks'),
     Input('clear-simulation-btn', 'n_clicks')],
    [State('month-selector', 'value'),
     State('duration-selector', 'value')]
)
def update_output(run_clicks, clear_clicks, selected_month, duration):
    ctx = dash.callback_context

    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'run-simulation-btn.n_clicks':
        simulation.run_simulation(rate=5, run=duration, month=selected_month)  # Adjust rate as needed
        gantt_chart = viz.gantt()  # Assuming this returns a figure object
        schedule_data = generate_schedule_table(simulation.schedule)
        return gantt_chart, schedule_data.to_dict('records')

    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'clear-simulation-btn.n_clicks':
        simulation.clear_simulation()
        schedule_data = generate_schedule_table(simulation.schedule)
        return go.Figure(), schedule_data.to_dict('records')

    # Initial load
    schedule_data = generate_schedule_table(simulation.schedule)
    return go.Figure(), schedule_data.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
