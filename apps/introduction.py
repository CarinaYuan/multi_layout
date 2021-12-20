from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
from dash import dash_table

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("ny_collision.csv"))
df=df.iloc[:,1:]

### pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

layout = html.Div([
    html.H1('Introduction', style={"textAlign": "center"}),
    html.Div([html.Img(src=app.get_asset_url('collision.png'))], style={'textAlign': 'center'}),
    html.Br(),
    dcc.Tabs(id="tabs-des", value='project', children=[
        dcc.Tab(label='Project Introduction', value='project'),
        dcc.Tab(label='Data Introduction', value='data'),
        dcc.Tab(label='Reference', value='reference'),
    ]),
    html.Div(id='content')
])

@app.callback(Output('content', 'children'),
              Input('tabs-des', 'value'))
def render_content(tab):
    if tab == 'project':
        return html.Div([
            html.Br(),
            dcc.Markdown('''
            
            **Welcome to New York City Vehicle Collision Analysis!!!**
            
            In this dashboard, you can explore the time and location changes in NYC vehicle collisions from 2015 to 2017.
            
            There are mainly two parts of the analysis:
            * *Time Analysis* includes yearly, monthly, weekly and hourly changes in the number of vehicle collisions in NYC.
            * *Location Analysis* includes vehicle collision distribution of different boroughs and street in NYC.
            
            Please click the options on left-side bar to choose the type of analysis you'd like to explore.
            
            Also, to better visualize and compare the changes, you can select the year or boroughs you'd like to put in each analysis.
            
            Let's try!!
            ''')

        ])
    elif tab == 'data':
        return html.Div([
            html.Br(),
            dcc.Markdown('''
            The vehicle collision data includes:
            
            * date and time,
            * location (borough, street names, zip code and latitude and longitude coordinates), 
            * injuries and fatalities,
            * vehicle number and types
            
            for the collisions in New York City during January 2015 and February 2017. 
            
            The original vehicle collision data was collected by the NYPD and published by NYC OpenData.
            '''),
            html.Hr(),
            html.H6('Sample Data Display:'),
            html.Div(generate_table(df))

        ])
    elif tab == 'reference':
        return html.Div([
            html.Br(),
            html.Label(['The original dataset is obtained from ', html.A('Kaggle', href='https://www.kaggle.com/nypd/vehicle-collisions',target='_blank'),'.']),
            html.Label(['New York City Borough Boundaries: ', html.A('click here',href='https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm',target='_blank'),'.']),
            html.Label(['Side Bar Construction Guidance ', html.A('click here',href='https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm',target='_blank'),'.'])
        ])





