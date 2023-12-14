import plotly.express as px

def generate_visuals_from_log():
    df = pd.read_csv('logs/assembly.csv')
    df['Timestamp_start'] = pd.to_datetime(df['Timestamp_start'])
    df['Timestamp_end'] = pd.to_datetime(df['Timestamp_end'])
    
    # Gantt Chart for Assemblies
    fig_gantt = px.timeline(df, x_start='Timestamp_start', x_end='Timestamp_end', y='Assembly', color='Vehicle')
    fig_gantt.update_layout(xaxis_title='Time', yaxis_title='Assembly', title='Assembly Timeline')

    # Station Utilization
    df['Duration'] = (df['Timestamp_end'] - df['Timestamp_start']).dt.total_seconds() / 3600  # Duration in hours
    fig_station = px.bar(df.groupby('Station')['Duration'].sum().reset_index(), x='Station', y='Duration')
    fig_station.update_layout(xaxis_title='Station', yaxis_title='Hours', title='Station Utilization')

    return fig_gantt, fig_station
@app.callback(
    [Output('gantt-chart', 'figure'),
     Output('station-utilization', 'figure'),  # Assuming you have a dcc.Graph with this ID
     # ... other outputs ... ],
    [Input('run-simulation-btn', 'n_clicks'),
     # ... other inputs ... ],
    [State('month-selector', 'value'),
     State('rate-input', 'value'),
     State('duration-selector', 'value')]
)
def update_output(run_clicks, clear_clicks, selected_month, rate, duration):
    # ... existing logic ...
    
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'run-simulation-btn.n_clicks':
        # ... simulation logic ...
        fig_gantt, fig_station = generate_visuals_from_log()
        return fig_gantt, fig_station,  # ... other return values ...

    # ... existing logic ...
dbc.Row(dbc.Col(dcc.Graph(id='gantt-chart', figure=go.Figure()), width=12)),
dbc.Row(dbc.Col(dcc.Graph(id='station-utilization', figure=go.Figure()), width=12)),
# ... other layout components ...
