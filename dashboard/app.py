import json
import os
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go

# Path to processed data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_FILE = os.path.join(BASE_DIR, "data", "processed", "processed_crypto.json")

# Initialize Dash app
app = Dash(__name__)
app.title = "Crypto Agent Dashboard"

# Layout
app.layout = html.Div(
    children=[
        html.H1("Real-Time Crypto Dashboard", style={"textAlign": "center"}),
        dcc.Graph(id="price-graph"),
        dcc.Interval(id="interval-component", interval=15*1000, n_intervals=0),  # refresh every 15 sec
        html.Div(id="last-update", style={"textAlign": "center", "marginTop": 20})
    ]
)

# Callback to update graph
@app.callback(
    Output("price-graph", "figure"),
    Output("last-update", "children"),
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    if not os.path.exists(PROCESSED_FILE):
        return {}, "Processed data not found yet."

    with open(PROCESSED_FILE, "r") as f:
        data = json.load(f)

    coins = list(data["prices"].keys())
    prices = [data["prices"][coin]["usd"] for coin in coins]
    percent_change = [data["prices"][coin]["percent_change_24h"] for coin in coins]

    # Create DataFrame for easier handling
    df = pd.DataFrame({
        "Coin": coins,
        "Price": prices,
        "24h Change (%)": percent_change
    })

    # Plot bar chart
    fig = go.Figure(
        data=[
            go.Bar(x=df["Coin"], y=df["Price"], text=df["24h Change (%)"], textposition="auto")
        ]
    )
    fig.update_layout(title="Crypto Prices (USD)", yaxis_title="Price USD", xaxis_title="Coin")

    return fig, f"Last updated: {pd.Timestamp.utcnow()} UTC"

# Run server
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # REQUIRED for Docker
        port=8050,
        debug=False
    )

