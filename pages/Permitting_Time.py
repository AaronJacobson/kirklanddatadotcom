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

kirkland_graph = px.line(
    data_frame=df[df["city"] == "Kirkland"],
    x="date",
    y="Median Permit Issue Time (Days)",
    color="city",
    line_shape="linear",
    title="Median New Single Family Permit Issue Time In Kirkland",
)
bellevue_graph = px.line(
    data_frame=df[df["city"] == "Bellevue"],
    x="date",
    y="Median Permit Issue Time (Days)",
    color="city",
    line_shape="linear",
    title="Median New Single Family Permit Issue Time In Bellevue",
)

layout = html.Div(
    children=[
        dcc.Markdown("# Permitting Time"),
        html.Hr(),
        dcc.Markdown(
            """
            One of the many sources of uncertainty for housing developers is the amount of time it takes to get a permit to build housing.
            In general, getting a building permit used to be relatively quick and easy, however permitting times have been increasing in recent years.
            While permitting times did skyrocket during the pandemic, this problem predates covid.


            For the purpose of this analysis, I'm measuring permitting time by calculating the number of days between the date a permit was issued and
             the date the permit application for that same permit was submitted.
            Due to data quality issues, this analysis only uses permit applications for new single family homes. I'll be primarily focusing on permitting
             data for the cities of Kirkland, WA and Bellevue, WA.

            ## Kirkland
            This graph of the median number of days between permit application and issue dates for new single family home permits over time in the City of
             Kirkland shows a few patterns:
            
            1. A slow increase from 1998 to 2003, peaking at a median permit time of  ~150 days.
            2. A sharp decrease in permitting time through 2003, reaching a median permit time of ~75 days.
            3. An increase to ~115 days in 2006 that holds until late 2009.
            4. A short bump from a baseline ~75 days to ~100 days that starts in July 2010 and returns to the baseline by December 2011.
            5. An increase starting mid 2013 that reachs ~100 days and stays there for 2015.
            6. A sharp increase starting in 2016 that levels off around ~150 days.
            7. Another sharp increase starting around June/July 2020 that hasn't stopped increasing with median permitting times as of July 2023 reaching over
             250 days.
            """
        ),
        dcc.Graph(id="kirkland_graph", figure=kirkland_graph),
        dcc.Markdown(
            """
            ## Bellevue
            This graph of the median number of days between permit application and issue dates for new single family home permits over time in the City of Bellevue 
            shows a few patterns:
            
            1. A decrease in permitting time in 2003, at roughly the same time as Kirkland's 2003 decrease.
            2. A drastic increase in permitting time starting in mid 2007, peaking in 2009, and returning the the previous baseline in 2010.
            3. A slow increase stretching from late 2012 to January 2016.
            4. Permitting times stayed roughly the same in Bellevue from January 2016 to September 2022.
            5. A drastic rise in permitting times starting in September 2022 with no end in sight as of July 2023.
            """
        ),
        dcc.Graph(id="bellevue_graph", figure=bellevue_graph),
        dcc.Markdown(
            """
            Some notes:
            
            1. Both Kirkland and Bellevue saw significant decreases in permitting time in 2003.
            2. Both Kirkland and Bellevue saw increases in permitting time around the 2008 crash, but with signficantly different magnitudes.
            3. Both Kirkland and Bellevue saw increases in permitting time around 2011, but Kirkland saw a larger increase.
            4. Both Kirkland and Bellevue saw increases in permitting time from 2012 to 2017 but Bellevue's permitting times started to increase about a year before 
            Kirkland. Additionally, in 2012, Kirkland had a lower median permitting time than Bellevue, but ended up at roughly the same place by 2017.
            5. Kirkland saw an increase in permitting times shortly after the pandemic hit, but Bellevue's permitting times didn't see a similar increase until 2022.
            """
        ),
        dcc.Markdown(
            """
            ## Other Cities
            Using public records requests, I obtained data on the permit application date and permit issue date for new construction single family permits in various 
            cities (among other permits). The graph below shows the median number of days between the permit application date and the permit issue date for all permits 
            in a 365 day lookback window from the date show on the x-axis.
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
