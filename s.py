# Initialize simulation
simulation = Simulation()

# Function to convert schedule data to a format suitable for Dash DataTable
def generate_table_data():
    data = []
    for (program, mbom), prog_obj in simulation.schedule.programs.items():
        row = {'Program': program, 'MBOM': mbom}
        for month in simulation.schedule.months:
            row[month] = prog_obj.get_quantity_for_month(month)
        data.append(row)
    return data

# Define the layout of the app
app.layout = html.Div([
    # Manufacturing Simulation Dashboard
    html.Div([
        html.H1("Manufacturing Simulation Dashboard"),
        html.H2("Program Schedule"),
        dash_table.DataTable(
            id='schedule-table',
            editable=True,
            columns=[{"name": "Program", "id": "Program"}, {"name": "MBOM", "id": "MBOM"}] +
                    [{"name": month, "id": month} for month in simulation.schedule.months],
            data=generate_table_data()
        ),
        html.Label('Rate', htmlFor='rate'),
        dcc.Input(id='rate', type='number', placeholder="Enter Rate", value=1, min=1, max=50),
        html.Label('Run Days', htmlFor='run'),
        html.Button("Run Simulation", id='run-simulation-button', className='button')
    ]),

    # Additional Simulation Analysis (hidden initially)
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Additional Simulation Analysis", className="text-center mb-4"), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='vehicle-dropdown',
                    options=[],  # Options will be set dynamically after simulation
                    value=None,
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
    ], fluid=True, style={'display': 'none'}, id='additional-analysis-container')
], style={'width': '90%', 'margin': 'auto'})

# Callback for running the simulation
@app.callback(
    Output('schedule-table', 'data'),
    Output('vehicle-dropdown', 'options'),
    Output('additional-analysis-container', 'style'),
    [Input('run-simulation-button', 'n_clicks')],
    [State('rate', 'value'), State('run', 'value')],
    prevent_initial_call=True
)
def update_simulation_and_graphs(n_clicks, rate, run):
    if n_clicks:
        # Run the simulation
        simulation.run_simulation(rate, run)

        # Update the DataTable
        new_data = generate_table_data()

        # Load and prepare new data for additional analysis
        df = pd.read_csv('simulation_data.csv')
        options = [{'label': v, 'value': v} for v in df['Vehicle'].unique()]

        return new_data, options, {'display': 'block'}

    return no_update, no_update, no_update

# Callbacks for additional graphs
# (Implement the rest of the callbacks here, similar to the original callbacks in your second code snippet)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
