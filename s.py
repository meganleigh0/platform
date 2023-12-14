def generate_schedule_table(schedule):
    # Placeholder function - replace with actual logic to generate a table from the schedule
    table_header = [html.Thead(html.Tr([html.Th("Program"), html.Th("Quantity per Month")]))]
    table_body = [html.Tr([html.Td(program), html.Td(quantity)]) for program, quantity in schedule.items()]
    return html.Table(table_header + table_body)
Step 2: Dash App Layout
python
Copy code
app.layout = html.Div([
    html.H1("Production Schedule Simulator"),
    html.Div(id='schedule-table', children=generate_schedule_table(simulation.schedule.programs)),
    dcc.Dropdown(
        id='month-selector',
        options=[{'label': month, 'value': month} for month in simulation.schedule.months],
        value='January 2024'
    ),
    dcc.RadioItems(
        id='duration-selector',
        options=[{'label': 'Day', 'value': 1}, {'label': 'Week', 'value': 7}, {'label': 'Month', 'value': 30}],
        value=1
    ),
    html.Button('Run Simulation', id='run-simulation-btn'),
    html.Button('Clear Simulation', id='clear-simulation-btn'),
    dcc.Graph(id='gantt-chart', figure=go.Figure())
])
Step 3: Callbacks for Simulation and Clearing
python
Copy code
@app.callback(
    [Output('gantt-chart', 'figure'),
     Output('schedule-table', 'children')],
    [Input('run-simulation-btn', 'n_clicks'),
     Input('clear-simulation-btn', 'n_clicks')],
    [State('month-selector', 'value'),
     State('duration-selector', 'value')]
)
def update_output(run_clicks, clear_clicks, selected_month, duration):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'run-simulation-btn' and run_clicks:
        simulation.run_simulation(rate, duration, selected_month)
        gantt_chart = viz.gantt()  # Assuming this returns a figure object
        return gantt_chart, generate_schedule_table(simulation.schedule.programs)

    elif button_id == 'clear-simulation-btn' and clear_clicks:
        # Clearing logic here
        return go.Figure(), generate_schedule_table(simulation.schedule.programs)

    return go.Figure(), generate_schedule_table(simulation.schedule.programs)
This setup:
