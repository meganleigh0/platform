from dash import Dash
from flask import Flask

server = Flask(__name__)
app = Dash(__name__, server=server, suppress_callback_exceptions=True)

from dash import html, dcc
import dash
from app import app
import pages.home as home
import pages.page1 as page1
import pages.page2 as page2

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Home | ', href='/'),
        dcc.Link('Page 1 | ', href='/page1'),
        dcc.Link('Page 2', href='/page2'),
    ], className='nav-bar'),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)

from dash import html

layout = html.Div([
    html.H1('Welcome to the Home Page')
])
