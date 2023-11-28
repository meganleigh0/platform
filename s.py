from dash.dependencies import Input, Output
from app import app
import pages.home as home
import pages.page1 as page1
import pages.page2 as page2

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    print(f"Current pathname: {pathname}")  # Print the current pathname

    if pathname == '/':
        print("Loading home layout")  # Debug print statement
        return home.layout()
    elif pathname == '/page1':
        print("Loading page 1 layout")  # Debug print statement
        return page1.layout()
    elif pathname == '/page2':
        print("Loading page 2 layout")  # Debug print statement
        return page2.layout()
    else:
        print("Loading 404 layout")  # Debug print statement
        return '404 Page Not Found'
