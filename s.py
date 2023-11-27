# Initialize the Dash app
app = dash.Dash(__name__)

# Initialize the Schedule object and load data
schedule = Schedule()
df = schedule.load_schedule()

# App layout
app.layout = html.Div([
    html.H1("Program Schedule"),
    dash_table.DataTable(id='schedule-table', columns=[{"name": i, "id": i} for i in df.columns], data=df.to_dict('records')),
    html.H3("Update Schedule"),
    dcc.Input(id='program-input', type='text', placeholder='Program Name'),
    dcc.Input(id='mbom-input', type='text', placeholder='MBOM'),
    dcc.Input(id='month-input', type='text', placeholder='Month'),
    dcc.Input(id='quantity-input', type='number', placeholder='Quantity'),
    html.Button('Update', id='update-button'),
    html.Div(id='update-output')
])

# Callback to update the table
@app.callback(
    Output('schedule-table', 'data'),
    [Input('update-button', 'n_clicks')],
    [State('program-input', 'value'),
     State('mbom-input', 'value'),
     State('month-input', 'value'),
     State('quantity-input', 'value')])
def update_schedule_display(n_clicks, program, mbom, month, quantity):
    if n_clicks:
        schedule.update_schedule(program, month, quantity)
    df = schedule.load_schedule()  # Reload the updated schedule
    return df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
