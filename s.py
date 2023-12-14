import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import simpy  # Ensure simpy is installed

# Import or define your Simulation, Schedule, and other classes here

simulation = Simulation()  # Create a simulation instance

def generate_calendar_style_schedule_table(schedule):
    data = []
    for program_key, program_obj in schedule.programs.items():
        program_name = program_key[0]
        for month, quantity in program_obj.production_plan.items():
            data.append({'Program': program_name, 'Month': month, 'Quantity': quantity})

    df = pd.DataFrame(data)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    pivot_df = df.pivot(index='Program', columns='Month', values='Quantity').fillna(0).reset_index()
    pivot_df = pivot_df[['Program'] + month_order]  # Ensure months are in correct order
    return pivot_df

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Production Schedule Simulator"), width=12)),
    dbc.Row(dbc.Col(dash_table.DataTable(id='schedule-table', columns=[], data=[], style_cell={'textAlign': 'center'}, style_header={'backgroundColor': 'rgb(210, 210, 210)', 'fontWeight': 'bold'}), width=12)),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='month-selector', options=[{'label': month, 'value': month} for month in simulation.schedule.months], value=simulation.schedule.months[0]), width=4),
        dbc.Col(dcc.RadioItems(id='duration-selector', options=[{'label': 'Day', 'value': 1}, {'label': 'Week', 'value': 7}, {'label': 'Month', 'value': 30}], value=1, inline=True), width=8),
    ]),
    dbc.Row([
        dbc.Col(html.Label("Rate:"), width=2),
        dbc.Col(dcc.Input(id='rate-input', type='number', value=5, placeholder='Enter Rate'), width=2),
        dbc.Col(dbc.Button('Run Simulation', id='run-simulation-btn', color="primary"), width=2),
        dbc.Col(dbc.Button('Clear Simulation', id='clear-simulation-btn', color="secondary"), width=2),
    ]),
    dbc.Row(dbc.Col(dcc.Graph(id='gantt-chart', figure=go.Figure()), width=12)),
    dbc.Row(dbc.Col(dcc.Loading(children=[html.Div(id='loading-output')], type='default'), width=12))
], fluid=True)

@app.callback(
    [Output('gantt-chart', 'figure'),
     Output('schedule-table', 'data'),
     Output('schedule-table', 'columns'),
     Output('loading-output', 'children')],
    [Input('run-simulation-btn', 'n_clicks'),
     Input('clear-simulation-btn', 'n_clicks')],
    [State('month-selector', 'value'),
     State('rate-input', 'value'),
     State('duration-selector', 'value')]
)
def update_output(run_clicks, clear_clicks, selected_month, rate, duration):
    ctx = dash.callback_context

    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'run-simulation-btn.n_clicks':
        simulation.run_simulation(rate, duration, selected_month)
        gantt_chart = viz.gantt()  # Replace with actual function to generate Gantt chart
        schedule_data = generate_calendar_style_schedule_table(simulation.schedule)
        columns = [{"name": i, "id": i} for i in schedule_data.columns]
        return gantt_chart, schedule_data.to_dict('records'), columns, "Simulation running..."

    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'clear-simulation-btn.n_clicks':
        simulation.clear_simulation()
        schedule_data = generate_calendar_style_schedule_table(simulation.schedule)
        columns = [{"name": i, "id": i} for i in schedule_data.columns]
        return go.Figure(), schedule_data.to_dict('records'), columns, ""

    schedule_data = generate_calendar_style_schedule_table(simulation.schedule)
    columns = [{"name": i, "id": i} for i in schedule_data.columns]
    return go.Figure(), schedule_data.to_dict('records'), columns, ""

if __name__ == '__main__':
    app.run_server(debug=True)
