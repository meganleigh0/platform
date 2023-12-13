import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load your data
df = pd.read_csv('simulation_data.csv')

# Calculate duration for the scatter plot
df['Duration'] = pd.to_datetime(df['Timestamp_end']) - pd.to_datetime(df['Timestamp_start'])
df['Duration'] = df['Duration'].dt.total_seconds() / 3600  # Convert duration to hours

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Manufacturing Simulation Dashboard", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='vehicle-dropdown',
                options=[{'label': v, 'value': v} for v in df['Vehicle'].unique()],
                value=df['Vehicle'].unique()[0],
                clearable=False,
                style={'width': '100%'}
            )
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

# Callback for the station utilization bar chart
@app.callback(
    Output('station-utilization-bar-chart', 'figure'),
    Input('vehicle-dropdown', 'value')
)
def update_station_bar_chart(vehicle):
    filtered_df = df[df['Vehicle'] == vehicle]
    station_count = filtered_df['Station'].value_counts()
    fig = px.bar(station_count, labels={'index': 'Station', 'value': 'Assembly Count'},
                 template="plotly_dark")
    fig.update_layout(transition_duration=500)
    return fig

# Callback for the assembly duration scatter plot
@app.callback(
    Output('assembly-duration-scatter-plot', 'figure'),
    Input('vehicle-dropdown', 'value')
)
def update_assembly_duration_scatter_plot(vehicle):
    filtered_df = df[df['Vehicle'] == vehicle]
    fig = px.scatter(filtered_df, x='Station', y='Duration', color='Assembly',
                     template="plotly_dark")
    fig.update_layout(transition_duration=500)
    return fig

# Callback for the workflow time series
@app.callback(
    Output('workflow-time-series', 'figure'),
    Input('vehicle-dropdown', 'value')
)
def update_workflow_time_series(vehicle):
    filtered_df = df[df['Vehicle'] == vehicle]
    fig = px.line(filtered_df, x='Timestamp_start', y='Assembly', template="plotly_dark")
    fig.update_layout(transition_duration=500)
    return fig

# Callback for the data table
@app.callback(
    Output('data-table', 'figure'),
    Input('vehicle-dropdown', 'value')
)
def update_data_table(vehicle):
    filtered_df = df[df['Vehicle'] == vehicle]
    fig = dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
