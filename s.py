from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from flask import Flask

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app
app = Dash(__name__, server=server, suppress_callback_exceptions=True)

# Define the navigation bar
navbar = html.Div([
    dcc.Link('Home', href='/'),
    dcc.Link('Page 1', href='/page1'),
    dcc.Link('Page 2', href='/page2'),
], className='navbar')

# Define the layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

# Define layouts for each page
def get_layout_home():
    return html.Div([
        html.H1("Welcome to the Home Page")
    ])

def get_layout_page1():
    return html.Div([
        html.H1("Dash App - Page 1")
    ])

def get_layout_page2():
    return html.Div([
        html.H1("Dash App - Page 2")
    ])

# Callback to update the page content
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return get_layout_page1()
    elif pathname == '/page2':
        return get_layout_page2()
    elif pathname in ['/', None]:
        return get_layout_home()
    return "404 Page Not Found"

if __name__ == '__main__':
    app.run_server(debug=True)
