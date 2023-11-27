@app.callback(
    Output('schedule-table', 'data'),
    [Input('update-button', 'n_clicks')],
    [State('program-dropdown', 'value'),
     State('mbom-dropdown', 'value'),  # Assuming you have a dropdown to select MBOM
     State('month-dropdown', 'value'),
     State('quantity-input', 'value')])
def update_schedule_display(n_clicks, program, mbom, month, quantity):
    if n_clicks:
        schedule.update_schedule(program, mbom, month, quantity)
    return generate_table_data()
