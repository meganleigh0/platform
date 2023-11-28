from dash import Dash
from flask import Flask

server = Flask(__name__)  # Create a Flask instance

app = Dash(__name__, server=server, suppress_callback_exceptions=True)  # Initialize Dash app

# Import layout and callbacks
from index import layout
app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)
