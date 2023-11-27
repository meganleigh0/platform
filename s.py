
app.layout = html.Div([
    html.H1("Program Schedule"),
    dcc.Graph(id='schedule-table'),
    html.H3("Update Schedule"),
    dcc.Input(id='program-input', type='text', placeholder='Program Name'),
    dcc.Input(id='mbom-input', type='text', placeholder='MBOM'),
    dcc.Input(id='month-input', type='text', placeholder='Month'),
    dcc.Input(id='quantity-input', type='number', placeholder='Quantity'),
    html.Button('Update', id='update-button'),
    html.Div(id='update-output')
])
Load and Display the Schedule:
Implement a function to load and display the schedule in a table format using Dash components.

python
Copy code
@app.callback(
    Output('schedule-table', 'figure'),
    [Input('update-button', 'n_clicks')],
    [State('program-input', 'value'),
     State('mbom-input', 'value'),
     State('month-input', 'value'),
     State('quantity-input', 'value')])
def update_schedule_display(n_clicks, program, mbom, month, quantity):
    schedule = Schedule()
    df = schedule.load_schedule()
    # Update the schedule if update button is clicked
    if n_clicks:
        schedule.update_schedule(program, month, quantity)
        df = schedule.load_schedule()  # Reload the updated schedule
    return {'data': [{'type': 'table', 'header': {'values': df.columns}, 'cells': {'values': df.values.T}}]}
# Update Functionality:
# Add functionality to update the schedule based on the user inputs.

@app.callback(
    Output('update-output', 'children'),
    [Input('update-button', 'n_clicks')],
    [State('program-input', 'value'),
     State('mbom-input', 'value'),
     State('month-input', 'value'),
     State('quantity-input', 'value')])
def update_schedule(n_clicks, program, mbom, month, quantity):
    if n_clicks:
        schedule = Schedule()
        schedule.update_schedule(program, month, quantity)
        return f"Updated {program} for {month} with quantity {quantity}."
    return ""
Run the App:
At the end of your script, add the following line to run the app.

python
Copy code
if __name__ == '__main__':
    app.run_server(debug=True)
