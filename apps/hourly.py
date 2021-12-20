from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("ny_collision.csv"))
df['YEAR']=df['YEAR'].apply(lambda x: str(x))

layout = html.Div([
    html.H1('Time Anlysis - Hourly', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Year:", style={"fontSize":"120%",'font-family':'Arial'}),
            dcc.Dropdown(
            id='year-dropdown_hour', value='2015', clearable=False,
            options=[{'label': x, 'value': x} for x in sorted(df.YEAR.unique())]
        )], className='three columns'),

        html.Div([
            html.Pre(children="Borough:", style={"fontSize":"120%",'font-family':'Arial'}),
            dcc.Checklist(
            id='borough-checklist_hour', value=['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND'],
            persistence=True, persistence_type='memory',
            options=[{'label': x.title(), 'value': x} for x in df.BOROUGH.unique()]
        )], className='five columns'),
    ], className='row'),

    dcc.Graph(id='hourly_line1', figure={}),
    dcc.Graph(id='hourly_line2', figure={}),

])

@app.callback(
    Output(component_id='hourly_line1', component_property='figure'),
    [Input(component_id='year-dropdown_hour', component_property='value'),
     Input(component_id='borough-checklist_hour', component_property='value')])
def display_value(year_chosen, borough_chosen):
    df_fltrd = df[(df['YEAR']==year_chosen)&(df.BOROUGH.isin(borough_chosen))]
    weekday_list=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    df_fltrd = df_fltrd[df_fltrd.DAY_of_WEEK.isin(weekday_list)]
    df_weekday= df_fltrd.groupby(['HOUR','BOROUGH']).size().reset_index(name='# of Vehicle Collisions')

    fig1 = px.line(df_weekday, x='HOUR', y='# of Vehicle Collisions', color='BOROUGH')
    fig1.update_layout(title_text='Hourly Change of The Number of Vehicle Collisions in NYC (Weekday)', title_x=0.5)
    #fig = fig.update_yaxes(tickprefix="$", ticksuffix="M")
    return fig1

@app.callback(
    Output(component_id='hourly_line2', component_property='figure'),
    [Input(component_id='year-dropdown_hour', component_property='value'),
     Input(component_id='borough-checklist_hour', component_property='value')])
def display_value(year_chosen, borough_chosen):
    df_fltrd = df[(df['YEAR']==year_chosen)&(df.BOROUGH.isin(borough_chosen))]
    weekend_list=["Saturday","Sunday"]
    df_fltrd=df_fltrd[df_fltrd.DAY_of_WEEK.isin(weekend_list)]
    df_weekend= df_fltrd.groupby(['HOUR','BOROUGH']).size().reset_index(name='# of Vehicle Collisions')

    fig2 = px.line(df_weekend, x='HOUR', y='# of Vehicle Collisions', color='BOROUGH')
    fig2.update_layout(title_text='Hourly Change of The Number of Vehicle Collisions in NYC (Weekend)', title_x=0.5)
    #fig = fig.update_yaxes(tickprefix="$", ticksuffix="M")
    return fig2
