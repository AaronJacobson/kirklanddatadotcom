import dash
from dash import dcc, html

dash.register_page(__name__)

layout = html.Div(
    [
        dcc.Markdown("# City Council Agenda Calendar"),
        html.Hr(),
        dcc.Markdown("Work in Progress")
    ]
)
