# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_parquet("https://kirklanddatastorage.blob.core.windows.net/kirklanddata/kirkland_sf_timeseries.parquet")
df["city"] = "Kirkland"

fig = px.line(
    data_frame=df,
    x="date",
    y="Median Permit Issue Time",
    color="city",
    # hover_name="city",
    line_shape="linear",
    title="Median New Single Family Permit Issue Time",
)

app.layout = html.Div(children=[
    html.H1(children='Kirkland Data'),

    # html.Div(children='''
    #     Dash: A web application framework for your data.
    # '''),

    dcc.Graph(
        id='sf_permitting_time_graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
