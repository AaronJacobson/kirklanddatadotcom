import dash
from dash import dcc, html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        dcc.Markdown(
            """
            Kirkland Data is a place for hosting interesting data analyses and projects relating to the Kirkland, Washington and the surrounding area.

            This website is built and maintained by Kirkland resident Aaron Jacobson. You can sign up for email alerts for whenever this site is updated by joining this google group: [https://groups.google.com/g/kirklanddata-updates](https://groups.google.com/g/kirklanddata-updates)

            You can get in contact with Aaron by:
            
            Email: aaron@kirklanddata.com
            
            LinkedIn: [https://www.linkedin.com/in/aaronljacobson/](https://www.linkedin.com/in/aaronljacobson/)
            
            Twitter: [https://twitter.com/AaronLJacobson](https://twitter.com/AaronLJacobson)

            """
        ),
    ]
)
