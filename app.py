# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.ZEPHYR])
server = app.server

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className="bg-light",
)
pages = dash.page_registry.values()
highlight_names = ["Council agenda calendar", "Permitting time"]
ignore_pages = ["Home"]
highlight_pages = []
other_pages = []
for page in pages:
    if page["name"] in ignore_pages:
        continue
    if page["name"] in highlight_names:
        highlight_pages.append(page)
    else:
        other_pages.append(page)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(page["name"], href=page["path"]))
        for page in highlight_pages
    ]
    + [
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.NavLink(
        #             [
        #                 html.Div(
        #                     page["name"], style={"color": "grey"}, className="ms-2"
        #                 ),
        #             ],
        #             href=page["path"],
        #             active="exact",
        #         )
        #         for page in other_pages
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="Other Projects",
        # ),
    ],
    brand="KirklandData",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = dbc.Container(
    [
        dbc.Row([dbc.Col([navbar])]),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [dash.page_container], xs=12, sm=12, md=12, lg=12, xl=12, xxl=12
                ),
            ]
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)
