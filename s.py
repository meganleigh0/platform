# App layout
app.layout = html.Div([
    # ... other components ...
    dcc.Dropdown(id='program-dropdown', options=[{'label': prog, 'value': prog} for prog, _ in schedule.programs.keys()], placeholder='Select Program'),
    dcc.Dropdown(id='month-dropdown', options=[{'label': month, 'value': month} for month in schedule.months], placeholder='Select Month'),
    dcc.Input(id='quantity-input', type='number', min=0, placeholder='Quantity'),
    html.Button('Update', id='update-button'),
    html.Div(id='update-output'),
    html.Button('-', id='decrement-button'),
    html.Button('+', id='increment-button')
])

# Callback for updating the quantity input based on program and month selection
@app.callback(
    Output('quantity-input', 'value'),
    [Input('program-dropdown', 'value'),
     Input('month-dropdown', 'value')])
def set_initial_quantity(program, month):
    if program and month:
        # Assuming program is the program name
        quantity = schedule.programs.get(program).get_quantity_for_month(month)
        return quantity
    return 0

# Callback to update the schedule and refresh the table
@app.callback(
    Output('schedule-table', 'data'),
    [Input('update-button', 'n_clicks'),
     Input('decrement-button', 'n_clicks'),
     Input('increment-button', 'n_clicks')],
    [State('program-dropdown', 'value'),
     State('month-dropdown', 'value'),
     State('quantity-input', 'value')],
    prevent_initial_call=True)
def update_schedule_display(update_clicks, decrement_clicks, increment_clicks, program, month, quantity):
    ctx = dash.callback_context
    if not ctx.triggered:
        return generate_table_data()
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'decrement-button':
        quantity = max(0, quantity - 1)
    elif button_id == 'increment-button':
        quantity += 1

    if program and month:
        schedule.update_schedule(program, month, quantity)

    return generate_table_data()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
