from dash import Dash
from flask import Flask

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app
app = Dash(__name__, server=server, suppress_callback_exceptions=True)

# Import the layout and register it with the app
from layouts import layout
app.layout = layout

# Run the app
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

# Define the layout
layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

from dash.dependencies import Input, Output
from app import app
import pages.page1, pages.page2  # Import other pages as needed

# Callback to update the page content
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return pages.page1.layout
    elif pathname == '/page2':
        return pages.page2.layout
    else:
        return "Welcome to the Home Page"
