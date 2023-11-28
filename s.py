from dash import Dash
from server import server

# Initialize the Dash app with external stylesheets if needed
app = Dash(__name__, server=server, suppress_callback_exceptions=True)

# Import the layout and callbacks
from index import app_layout
app.layout = app_layout

# Setup the callbacks (this is important to make sure all callbacks are loaded)
import pages.page1  # Make sure to import all pages that contain callbacks
import pages.page2

if __name__ == '__main__':
    app.run_server(debug=True)
