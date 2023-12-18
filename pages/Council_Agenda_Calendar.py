import dash
from dash import dcc, html

dash.register_page(__name__)

layout = html.Div(
    [
        dcc.Markdown("# City Council Agenda Calendar"),
        html.Hr(),
        dcc.Markdown(
            """
            The City of Kirkland maintains a calendar tracking subjects that the City Council will discuss in future meetings. This calendar is not an official notice and is subject to frequent change, but still shows what the City Council will be discussing up to months in advance.

            The current agenda calendar can be found here: [https://www.kirklandwa.gov/files/sharedassets/public/city-council/agenda-calendar/ccsched.pdf](https://www.kirklandwa.gov/files/sharedassets/public/city-council/agenda-calendar/ccsched.pdf)
            Unfortunately, the city does not send notifications when this calendar is updated.
            
            I've created a system to regularly check the agenda calendar and send email summaries of changes whenever updates are published. You can sign up to receive these emails by adding yourself to this Google Group: [https://groups.google.com/g/kirkland-council-agenda-calendar-updates](https://groups.google.com/g/kirkland-council-agenda-calendar-updates)
            
            The only emails this group will be used for are the automated agenda calendar summary emails which happen about 4 times a month. 
            
            Here is an example of what the beginning of those emails look like:
            """
        ),
        html.Img(src="assets/council_agenda_calendar_email.png", style={"width": "613px", "height": "786px"}),
    ]
)
