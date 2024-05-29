import dash
from dash import html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# Sample DataFrame setup
data = {
    'PartNumber': ['1234', '5678', '91011'],
    'Description': ['Widget A', 'Widget B', 'Widget C'],
    'Qty': [10, 20, 15],
    'Station': ['A1', 'A2', 'A3'],
    'Operations': [
        [['Op1', 30, 'Dept1'], ['Op2', 45, 'Dept2']],
        [],
        [['Op3', 60, 'Dept3']]
    ],
    'Variant': ['V1', 'V2', 'V1']
}

df = pd.DataFrame(data)

# Expanding the Operations column into multiple rows
df_exploded = df.explode('Operations')

# Creating separate columns for operation name, time, and department
def operation_details(operation):
    if operation:
        return {'OperationName': operation[0], 'Time': operation[1], 'Department': operation[2]}
    else:
        return {'OperationName': 'No Operations', 'Time': '-', 'Department': '-'}

df_exploded[['OperationName', 'Time', 'Department']] = df_exploded['Operations'].apply(operation_details).apply(pd.Series)
df_exploded.drop('Operations', axis=1, inplace=True)

# Dash app setup
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dcc.Dropdown(
        id='variant-selector',
        options=[{'label': i, 'value': i} for i in df_exploded['Variant'].unique()],
        value=df_exploded['Variant'].unique()[0],
        clearable=False
    ),
    dcc.Dropdown(
        id='station-selector',
        options=[{'label': i, 'value': i} for i in df_exploded['Station'].unique()],
        value=df_exploded['Station'].unique()[0],
        clearable=False
    ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df_exploded.columns],
        data=df_exploded.to_dict('records'),
        style_table={'height': '300px', 'overflowY': 'auto'}
    )
], fluid=True)

@app.callback(
    Output('table', 'data'),
    [Input('variant-selector', 'value'),
     Input('station-selector', 'value')]
)
def update_table(selected_variant, selected_station):
    filtered_df = df_exploded[(df_exploded['Variant'] == selected_variant) & (df_exploded['Station'] == selected_station)]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)