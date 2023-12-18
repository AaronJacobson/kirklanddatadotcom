import dash
from dash import dcc, html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        dcc.Markdown("# KirklandData.com"),
        dcc.Markdown("Work In Progress"),
    ]
)
