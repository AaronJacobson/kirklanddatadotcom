import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html
from plotly.subplots import make_subplots

from pages.config import PERMIT_TIME_URL

dash.register_page(__name__)

df = pd.read_parquet(PERMIT_TIME_URL).rename(
    {
        "Median Permit Issue Time": "Median Permit Issue Time (Days)",
    },
    axis=1,
)
df = df[df["city"] != "Auburn"]

made_by_watermark = go.layout.Template()
made_by_watermark.layout.annotations = [
    {
        "name": "made_by_watermark",
        "text": "Made by Aaron Jacobson, aaron@kirklanddata.com",
        "opacity": 0.75,
        "font": {"color": "black", "size": 12},
        "xref": "paper",
        "yref": "paper",
        "x": 0.5,
        "y": 0.95,
        "showarrow": False,
    }
]

kirkland_graph = px.line(
    data_frame=df[df["city"] == "Kirkland"],
    x="date",
    y="Median Permit Issue Time (Days)",
    color="city",
    line_shape="linear",
    title="Median New Single Family Permit Issue Time In Kirkland",
)
kirkland_graph.update_layout(template=made_by_watermark)
bellevue_graph = px.line(
    data_frame=df[df["city"] == "Bellevue"],
    x="date",
    y="Median Permit Issue Time (Days)",
    color="city",
    line_shape="linear",
    title="Median New Single Family Permit Issue Time In Bellevue",
)
bellevue_graph.update_layout(template=made_by_watermark)
full_timing_graph = px.line(
    data_frame=df,
    x="date",
    y="Median Permit Issue Time (Days)",
    color="city",
    line_shape="linear",
    title="Median New Single Family Permit Issue Time",
)
full_timing_graph.update_layout(template=made_by_watermark)
full_timing_graph.update_traces(visible="legendonly")
full_timing_graph.data[3].visible = True
full_applications_graph = px.line(
    data_frame=df,
    x="date",
    y="Number of Applications",
    color="city",
    line_shape="linear",
    title="Number of New Single Family Permit Applications in the Last Year",
)
full_applications_graph.update_traces(visible="legendonly")
full_applications_graph.data[3].visible = True
full_applications_graph.update_layout(template=made_by_watermark)

df_issaquah_timing = df[df["city"] == "Issaquah"].copy()
df_issaquah_timing["color"] = "Permit Issue Time"
issaquah_timing = px.line(
    data_frame=df_issaquah_timing,
    x="date",
    y="Median Permit Issue Time (Days)",
    color="color",
    line_shape="linear",
    title="Issaquah Median New Single Family Permit Issue Time In Issaquah",
)
df_issaquah_applications = df[df["city"] == "Issaquah"]
df_issaquah_applications["color"] = "Number of Applications"
issaquah_applications = px.line(
    data_frame=df_issaquah_applications,
    x="date",
    y="Number of Applications",
    color="color",
    line_shape="linear",
    title="Issaquah: Number of New Single Family Permit Applications in the Last Year",
)

issaquah_double_fig = make_subplots(specs=[[{"secondary_y": True}]])
issaquah_applications.update_traces(yaxis="y2")
issaquah_double_fig.add_traces(issaquah_timing.data + issaquah_applications.data)
issaquah_double_fig.update_layout(
    title="Issaquah: Permit Issue Time vs. Number of Applications",
    yaxis=dict(title="Median Permit Issue Time (Days)"),
    yaxis2=dict(title="Number of Applications"),
)
issaquah_double_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
issaquah_double_fig.update_layout(template=made_by_watermark)
drop_down = dcc.Dropdown(
    id="city_combined_dropdown",
    options=[{"label": city, "value": city} for city in df["city"].unique()],
    value="Kirkland",
    className="city_combined_container",
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
            the date the permit application for that same permit was submitted. Then for each date, take January 1st, 2023 as an example, I calculate 
            the median number of days between the permit application date and permit issue date for all permits issued up to 365 days before the chosen date. 
            So the data for January 1st, 2023 shows median number of days it took to get a permit for all permits issued from January 1st, 2022 to January 1st 2023.
            Due to data quality issues, this analysis only uses permit applications for new single family homes. I'll be primarily focusing on permitting data for the 
            cities of Kirkland, WA and Bellevue, WA.

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
        dcc.Graph(id="full_timing_graph", figure=full_timing_graph),
        dcc.Markdown(
            """
            ## Number of Applications
            A large number of applications submitted in a short window could explain the (short term) spikes we've seen in permit issue times in various cities. However,
            the number of single family permit applications seen in each jurisdiction doesn't explain all of the variation in permit issue time.

            Issaquah, for example, saw a large number of applications for single family permits from 2003 to 2006 but didn't see a large increase in permit issue times 
            until 2008.
            """
        ),
        dcc.Graph(id="issaquah_combined_plot", figure=issaquah_double_fig),
        dcc.Markdown(
            """
            In general, the difference in the exact timing of increases in applications and increases in permitting times suggest other factors such as staffing and/or 
            policy changes have a bigger impact of permitting timelines than just the volume of single family permit applications.
            """
        ),
        drop_down,
        dcc.Graph(id="combined_plot"),
        dcc.Markdown(
            """
            For completeness, here is a graph that allows you to compare the number of single family permit applications across jurisdictions over time.
            """
        ),
        dcc.Graph(id="full_applications_graph", figure=full_applications_graph),
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
    Output(component_id="combined_plot", component_property="figure"),
    [Input(component_id="city_combined_dropdown", component_property="value")],
)
def update_combined_graph(option_chosen):
    df_filtered = df[df["city"] == option_chosen]
    df_filtered_timing = df_filtered[["date", "Median Permit Issue Time (Days)"]].copy()
    df_filtered_timing["color"] = "Permit Issue Time"
    df_filtered_applications = df_filtered[["date", "Number of Applications"]].copy()
    df_filtered_applications["color"] = "Number of Applications"

    timing_graph = px.line(
        data_frame=df_filtered_timing,
        x="date",
        y="Median Permit Issue Time (Days)",
        color="color",
        line_shape="linear",
        title="Median New Single Family Permit Issue Time In Kirkland",
    )
    applications_graph = px.line(
        data_frame=df_filtered_applications,
        x="date",
        y="Number of Applications",
        color="color",
        line_shape="linear",
        title="Number of New Single Family Permit Applications in the Last Year",
    )
    subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])
    applications_graph.update_traces(yaxis="y2")
    subplot_fig.add_traces(timing_graph.data + applications_graph.data)
    subplot_fig.update_layout(
        title=f"{option_chosen}: Permit Issue Time vs. Number of Applications",
        yaxis=dict(title="Median Permit Issue Time (Days)"),
        yaxis2=dict(title="Number of Applications"),
    )
    subplot_fig.update_layout(template=made_by_watermark)
    subplot_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    return subplot_fig
