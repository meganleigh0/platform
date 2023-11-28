app.py
from dash import Dash
from flask import Flask
from layouts import layout
import callbacks  # Import callbacks to ensure they are registered

server = Flask(__name__)
app = Dash(__name__, server=server, suppress_callback_exceptions=True)
app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)

layouts.py
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

callbakcs.py
from dash.dependencies import Input, Output
from app import app
import page_layouts

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page1':
        return page_layouts.page1_layout()
    elif pathname == '/page2':
        return page_layouts.page2_layout()
    elif pathname in ['/', None]:
        return page_layouts.home_layout()
    return "404 Page Not Found"


from dash import html

def home_layout():
    return html.Div([
        html.H1("Welcome to the Home Page")
    ])

def page1_layout():
    return html.Div([
        html.H1("Dash App - Page 1")
    ])

def page2_layout():
    return html.Div([
        html.H1("Dash App - Page 2")
    ])

