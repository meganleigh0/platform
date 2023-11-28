from dash import html, dcc
from dash.dependencies import Input, Output
from app import app
import pages.page1, pages.page2  # Import other pages as needed

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
