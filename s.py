import dash
from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Assuming the Simulation class and its dependencies are defined and imported
from your_simulation_module import Simulation  # Replace with your actual import

# Initialize the Simulation instance
simulation = Simulation()

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load initial data
df = pd.read_csv('simulation_data.csv')

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Manufacturing Simulation Dashboard", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': month, 'value': month} for month in simulation.schedule.months.unique()],
                value=simulation.schedule.months.unique()[0],
                clearable=False,
                style={'width': '100%'}
            ),
            dcc.Input(id='rate-input', type='number', placeholder='Enter rate', style={'width': '100%', 'margin': '10px 0'}),
            dcc.Input(id='run-input', type='number', placeholder='Enter run quantity', style={'width': '100%', 'margin': '10px 0'}),
            html.Button('Run Simulation', id='run-simulation-button', n_clicks=0, className='btn btn-primary', style={'width': '100%'})
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='station-utilization-bar-chart'), width=6),
        dbc.Col(dcc.Graph(id='assembly-duration-scatter-plot'), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='workflow-time-series'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='data-table'), width=12)
    ])
], fluid=True)

# Callback for running the simulation
@app.callback(
    Output('station-utilization-bar-chart', 'figure'),
    Output('assembly-duration-scatter-plot', 'figure'),
    Output('workflow-time-series', 'figure'),
    Output('data-table', 'figure'),
    Input('run-simulation-button', 'n_clicks'),
    State('month-dropdown', 'value'),
    State('rate-input', 'value'),
    State('run-input', 'value'),
    prevent_initial_call=True
)
def run_simulation_and_update_plots(n_clicks, month, rate, run):
    if n_clicks > 0:
        simulation.run_simulation(rate, run, month)
        # Reload the data
        df = pd.read_csv('simulation_data.csv')

        # Generate updated plots
        station_count = df['Station'].value_counts()
        bar_chart = px.bar(station_count, labels={'index': 'Station', 'value': 'Assembly Count'})

        df['Duration'] = pd.to_datetime(df['Timestamp_end']) - pd.to_datetime(df['Timestamp_start'])
        df['Duration'] = df['Duration'].dt.total_seconds() / 3600
        scatter_plot = px.scatter(df, x='Station', y='Duration', color='Assembly')

        time_series = px.line(df, x='Timestamp_start', y='Assembly')

        data_table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        return bar_chart, scatter_plot, time_series, data_table

    raise dash.exceptions.PreventUpdate

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
