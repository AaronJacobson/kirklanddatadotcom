import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dcc, html

from pages.config import PERMIT_TIME_URL

dash.register_page(__name__)

df = pd.read_parquet(PERMIT_TIME_URL).rename(
    {
        "Median Permit Issue Time": "Median Permit Issue Time (Days)",
    },
    axis=1,
)
df = df[df["city"] != "Auburn"]

check_list = dcc.Checklist(
    id="city_checklist",
    options=[{"label": city, "value": city} for city in df["city"].unique()],
    value=["Kirkland"],
    className="city_container",
    inputClassName="city_input",
    labelClassName="label_input",
)

layout = html.Div(
    children=[
        dcc.Markdown("# Permitting Time"),
        html.Hr(),
        dcc.Markdown(
            """
            Using public records requests, I obtained data on the permit application date and permit issue date for new construction single family permits in various cities (among other permits).
            The graph below shows the median number of days between the permit application date and the permit issue date for all permits in a 365 day lookback window from the
            date show on the x-axis.
            """
        ),
        check_list,
        dcc.Graph(id="sf_permitting_time_graph"),
        dcc.Markdown(
            """
            The data shown here comes from public records requests submitted around June/July 2023.

            In my public records requests, I was able to get the permitting data for all permits in the various cities' databases, including multifamily permits.
            However, these cities see so few multifamily permits that it's difficult to make a trustworthy graph showing the permitting time for multifamily permits.
            """
        ),
        html.Hr(),
        dcc.Markdown(
            """
            If you have any questions and/or would like to see the original permit data used for this analysis, please reach out to me at aaron@kirklanddata.com
            """
        ),
    ]
)


@callback(
    Output(component_id="sf_permitting_time_graph", component_property="figure"),
    [Input(component_id="city_checklist", component_property="value")],
)
def update_graph(options_chosen):
    df_filtered = df[df["city"].isin(options_chosen)]

    line_chart = px.line(
        data_frame=df_filtered,
        x="date",
        y="Median Permit Issue Time (Days)",
        color="city",
        line_shape="linear",
        title="Median New Single Family Permit Issue Time",
    )

    return line_chart
