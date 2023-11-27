import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from analysis import visualization as viz
from sim import main

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Manufacturing Simulation Dashboard"),
    html.Button("Run Simulation", id='run-simulation-button'),
    dcc.Graph(id='gantt-chart'),
    dcc.Graph(id='department-graph')
])

# Callback for running the simulation
@app.callback(
    [Output('gantt-chart', 'figure'),
     Output('department-graph', 'figure')],
    [Input('run-simulation-button', 'n_clicks')]
)
def update_output(n_clicks):
    if n_clicks is not None:
        # Run the simulation
        main.run_simulation()
        # Generate visualizations
        gantt_chart = viz.gantt()
        department_graph = viz.department_graph()
        return gantt_chart, department_graph
    return dash.no_update

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
