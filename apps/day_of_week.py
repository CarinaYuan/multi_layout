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
    html.H1('Time Anlysis - Weekly', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Year:", style={"fontSize":"120%",'font-family':'Arial'}),
            dcc.Dropdown(
            id='year-dropdown_week', value='2015', clearable=False,
            options=[{'label': x, 'value': x} for x in sorted(df.YEAR.unique())]
        )], className='three columns'),

        html.Div([
            html.Pre(children="Borough:", style={"fontSize":"120%",'font-family':'Arial'}),
            dcc.Checklist(
            id='borough-checklist_week', value=['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND'],
            persistence=True, persistence_type='memory',
            options=[{'label': x.title(), 'value': x} for x in df.BOROUGH.unique()]
        )], className='five columns'),
    ], className='row'),

    dcc.Graph(id='weekly_line', figure={}),
])

@app.callback(
    Output(component_id='weekly_line', component_property='figure'),
    [Input(component_id='year-dropdown_week', component_property='value'),
     Input(component_id='borough-checklist_week', component_property='value')])
def display_value(year_chosen, borough_chosen):
    df_fltrd = df[(df['YEAR']==year_chosen)&(df.BOROUGH.isin(borough_chosen))]
    df_weekly= df_fltrd.groupby(['DAY_of_WEEK','BOROUGH']).size().reset_index(name='# of Vehicle Collisions')
    day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"]
    df_weekly.index = pd.CategoricalIndex(df_weekly['DAY_of_WEEK'],categories=day_of_week,ordered=True)
    df_weekly=df_weekly.sort_index()
    fig = px.line(df_weekly, x='DAY_of_WEEK', y='# of Vehicle Collisions', color='BOROUGH')
    fig.update_layout(title_text='Weekly Change of The Number of Vehicle Collisions in NYC', title_x=0.5)
    #fig = fig.update_yaxes(tickprefix="$", ticksuffix="M")
    return fig
