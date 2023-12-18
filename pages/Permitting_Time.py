import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html

from pages.config import PERMIT_TIME_URL

dash.register_page(__name__)

df = pd.read_parquet(PERMIT_TIME_URL)
df["city"] = "Kirkland"

fig = px.line(
    data_frame=df,
    x="date",
    y="Median Permit Issue Time",
    color="city",
    line_shape="linear",
    title="Median New Single Family Permit Issue Time in Days",
)
layout = html.Div(
    children=[
        dcc.Markdown("# Permitting Time (WIP)"),
        html.Hr(),
        # dcc.Markdown("Work In Progress"),
        dcc.Graph(id="sf_permitting_time_graph", figure=fig),
    ]
)
