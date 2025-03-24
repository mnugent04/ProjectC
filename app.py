from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

# Initialize app with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# Set layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
