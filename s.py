import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State

# Initialize the Dash app
app = dash.Dash(__name__)

# Initialize the Schedule object and load data
schedule = Schedule()
schedule.load_schedule()  # Load initial data into the schedule

# Function to convert schedule data to a format suitable for Dash DataTable
def generate_table_data():
    data = []
    for (program, mbom), prog_obj in schedule.programs.items():
        row = {'Program': program, 'MBOM': mbom}
        for month in schedule.months:
            row[month] = prog_obj.get_quantity_for_month(month)
        data.append(row)
    return data

# App layout
app.layout = html.Div([
    html.H1("Program Schedule"),
    dash_table.DataTable(id='schedule-table', columns=[{"name": "Program", "id": "Program"}, {"name": "MBOM", "id": "MBOM"}] + [{"name": month, "id": month} for month in schedule.months]),
    html.H3("Update Schedule"),
    dcc.Input(id='program-input', type='text', placeholder='Program Name'),
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
     State('month-input', 'value'),
     State('quantity-input', 'value')])
def update_schedule_display(n_clicks, program, month, quantity):
    if n_clicks:
        schedule.update_schedule(program, month, quantity)
    return generate_table_data()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
