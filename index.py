from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import introduction, yearly, monthly, day_of_week, hourly, location

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "22rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("NYC Vehicle Collision Analysis", className="display-4",style={"textAlign": "center"}),
        html.Hr(),
        html.P(
            "Please click on the analysis of NYC vehicle collision that you are interested in!! :)", className="lead"
        ),
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink("Introduction", href="/", active="exact",style={"textAlign": "center"}),
                dbc.NavLink("Yearly Analysis", href="/apps/yearly", active="exact",style={"textAlign": "center"}),
                dbc.NavLink("Monthly Analysis", href="/apps/monthly", active="exact",style={"textAlign": "center"}),
                dbc.NavLink("Weekly Analysis", href="/apps/weekly", active="exact",style={"textAlign": "center"}),
                dbc.NavLink("Hourly Analysis", href="/apps/hourly", active="exact",style={"textAlign": "center"}),
                dbc.NavLink("Location Analysis", href="/apps/location", active="exact",style={"textAlign": "center"})

            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        dcc.Markdown('''
        > MA705 Data Sceinece
        
        >@Zehui Yuan
        
        >Bentley University
        
        >MSBA 2022
        ''')

    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content",
                   children=[],
                   style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return introduction.layout
    if pathname == '/apps/yearly':
        return yearly.layout
    if pathname == '/apps/monthly':
        return monthly.layout
    if pathname == '/apps/weekly':
        return day_of_week.layout
    if pathname == '/apps/hourly':
        return hourly.layout
    if pathname == '/apps/location':
        return location.layout



if __name__ == '__main__':
    app.run_server(debug=False)
