from dash import Dash
from flask import Flask
from index import layout
import callbacks  # Ensure callbacks are registered

server = Flask(__name__)
app = Dash(__name__, server=server, suppress_callback_exceptions=True)
app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)

from dash import html, dcc

# Define the navigation bar
navbar = html.Div([
    dcc.Link('Home', href='/'),
    dcc.Link('Page 1', href='/page1'),
    dcc.Link('Page 2', href='/page2'),
    # Add more links as needed
], className='navbar')

# Main layout of the app
layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

from dash import html

def layout():
    return html.Div([
        html.H1('Dash App - Page 1'),
        # Add more components for Page 1 here
    ])
from dash.dependencies import Input, Output
from app import app
from pages import home, page1, page2

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return home.layout()
    elif pathname == '/page1':
        return page1.layout()
    elif pathname == '/page2':
        return page2.layout()
    return '404 Page Not Found'
