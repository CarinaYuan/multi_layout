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

layout = html.Div([
    html.H1('Time Anlysis - Yearly', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Borough:", style={"fontSize": "120%",'font-family':'Arial'}),
            dcc.Checklist(
            id='borough_checklist',
            persistence=True, persistence_type='memory',
            options=[{'label':'Bronx','value':'BRONX'},
                     {'label':'Brooklyn','value':'BROOKLYN'},
                     {'label':'Manhattan','value':'MANHATTAN'},
                     {'label':'Queens','value':'QUEENS'},
                     {'label':'Staten Island','value':'STATEN ISLAND'}],
            value=['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND'])])],
        className='row'),

    dcc.Graph(id='yearly_line', figure={}),
])

@app.callback(
    Output(component_id='yearly_line', component_property='figure'),
    [Input(component_id='borough_checklist', component_property='value')]
)
def display_value(borough_chosen):
    df_fltrd = df[df.BOROUGH.isin(borough_chosen)]
    df_yearly= df_fltrd.groupby(['YEAR','BOROUGH']).size().reset_index(name='# of Vehicle Collisions')
    fig = px.line(df_yearly, x='YEAR', y='# of Vehicle Collisions', color='BOROUGH')
    fig.update_layout(title_text='Yearly Change of The Number of Vehicle Collisions in NYC (2015-2017)', title_x=0.5)
    #fig = fig.update_yaxes(tickprefix="$", ticksuffix="M")
    return fig
