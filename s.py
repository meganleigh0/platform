import dash
from dash import dcc, html, dash_table, Output, Input, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from your_simulation_module import Simulation  # Replace with your actual simulation module
from your_visualization_module import viz  # Replace with your actual visualization module

# Initialize simulation
simulation = Simulation()

# Initialize Dash app
app = dash.Dash(__name__)

# Read initial DataFrame
df = pd.read_csv('logs/assembly.csv')

# Function to convert schedule data to a format suitable for Dash DataTable
def generate_table_data():
    data = []
    for (program, mbom), prog_obj in simulation.schedule.programs.items():
        row = {'Program': program, 'MBOM': mbom}
        for month in simulation.schedule.months:
            row[month] = prog_obj.get_quantity_for_month(month)
        data.append(row)
    return data

data = generate_table_data()

# Dash app layout
app.layout = html.Div([
    html.Div([
        html.H1("Manufacturing Simulation Dashboard"),
        html.H2("Program Schedule")
    ]),
    html.Div([
        dash_table.DataTable(
            id='schedule-table',
            editable=True,
            columns=[{"name": "Program", "id": "Program"}, {"name": "MBOM", "id": "MBOM"}] +
                    [{"name": month, "id": month} for month in simulation.schedule.months],
            data=data
        ),
        html.Label('Rate', htmlFor='rate'),
        dcc.Input(id='rate', type='number', placeholder="Enter Rate", value=1, min=1, max=50),
        html.Label('Run Days', htmlFor='run'),
        html.Button("Run Simulation", id='run-simulation-button', className='button')
    ]),
    html.Div([
        dcc.Graph(id='gantt-chart'),
        dcc.Graph(id='department-graph'),
        dcc.Dropdown(
            id='vehicle-dropdown',
            options=[{'label': v, 'value': v} for v in df['Vehicle'].unique()],
            value=df['Vehicle'].unique()[0],
            clearable=False,
            style={'width': '100%'}
        ),
        dcc.Graph(id='station-utilization-bar-chart'),
        dcc.Graph(id='assembly-duration-scatter-plot'),
        dcc.Graph(id='workflow-time-series'),
        dcc.Graph(id='data-table')
    ], id='div-charts-01', style={'display': 'none'}),
    html.Div(id='hidden-div', style={'display': 'none'})  # Hidden div for storing DataFrame
])

# Callback for running the simulation
@app.callback(
    [Output('gantt-chart', "figure"),
     Output("department-graph", "figure"),
     Output('div-charts-01', 'style'),
     Output('hidden-div', 'children')],
    [Input('run-simulation-button', 'n_clicks')],
    [State("rate", 'value'), State('run', "value")]
)
def update_output(n_clicks, rate, run):
    if n_clicks is not None:
        simulation.run_simulation(rate, run)
        gantt_chart = viz.gantt()
        department_graph = viz.department_utilization()
        df = pd.read_csv('logs/assembly.csv')
        return gantt_chart, department_graph, {'display': 'block'}, df.to_json(date_format='iso', orient='split')
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Callbacks for updating graphs
@app.callback(
    Output('station-utilization-bar-chart', 'figure'),
    [Input('vehicle-dropdown', 'value'),
     Input('hidden-div', 'children')]
)
def update_station_bar_chart(vehicle, jsonified_df):
    if jsonified_df is None:
        raise dash.exceptions.PreventUpdate
    df = pd.read_json(jsonified_df, orient='split')
    filtered_df = df[df['Vehicle'] == vehicle]
    station_count = filtered_df['Station'].value_counts()
    fig = px.bar(station_count, labels={'index': 'Station', 'value': 'Assembly Count'}, template="plotly_dark")
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('assembly-duration-scatter-plot', 'figure'),
    [Input('vehicle-dropdown', 'value'),
     Input('hidden-div', 'children')]
)
def update_assembly_duration_scatter_plot(vehicle, jsonified_df):
    if jsonified_df is None:
        raise dash.exceptions.PreventUpdate
    df = pd.read_json(jsonified_df, orient='split')
    filtered_df = df[df['Vehicle'] == vehicle]
    fig = px.scatter(filtered_df, x='Station', y='Duration', color='Assembly', template="plotly_dark")
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('workflow-time-series', 'figure'),
    [Input('vehicle-dropdown', 'value'),
     Input('hidden-div', 'children')]
)
def update_workflow_time_series(vehicle, jsonified_df):
    if jsonified_df is None:
        raise dash.exceptions.PreventUpdate
    df = pd.read_json(jsonified_df, orient='split')
    filtered_df = df[df['Vehicle'] == vehicle]
    fig = px.line(filtered_df, x='Timestamp_start', y='Assembly', template="plotly_dark")
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('data-table', 'figure'),
    [Input('vehicle-dropdown', 'value'),
     Input('hidden-div', 'children')]
)
def update_data_table(vehicle, jsonified_df):
    if jsonified_df is None:
        raise dash.exceptions.PreventUpdate
    df = pd.read_json(jsonified_df, orient='split')
    filtered_df = df[df['Vehicle'] == vehicle]
    fig = dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
