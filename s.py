import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Import your custom Schedule class
from schedule import Schedule

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Instantiate your Schedule class
schedule = Schedule()
schedule_df = schedule.load_schedule()  # Assuming this returns a DataFrame

# Dash Layout
app.layout = html.Div([
    dbc.Container([
        html.H1('Production Schedule'),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': month, 'value': month} for month in schedule.months],
                    value=schedule.months[0]
                )
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id='schedule-table')
            ]),
        ]),
        # Add more components as needed for your interactivity
    ])
])

# Callback for updating the table
@app.callback(
    Output('schedule-table', 'children'),
    [Input('month-dropdown', 'value')]
)
def update_table(selected_month):
    filtered_df = schedule_df[schedule_df['Month'] == selected_month]
    return dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
