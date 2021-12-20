from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
from dash import dash_table
import plotly.graph_objects as go

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("ny_collision.csv"))
df['YEAR']=df['YEAR'].apply(lambda x: str(x))
#geo_df = gpd.GeoDataFrame(df, crs="EPSG:4326",
                                #geometry=gpd.points_from_xy(df.LONGITUDE, df.LATITUDE))
#ny = gpd.read_file(DATA_PATH.joinpath("nybb.geojson"))


layout = html.Div([
    html.H1('Location Analysis - Borough & Street', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Year", style={"fontSize": "120%",'font-family':'Arial'}),
            dcc.Dropdown(
            id='year-dropdown_location', value='2015', clearable=False,
            options=[{'label': x, 'value': x} for x in sorted(df.YEAR.unique())]
        )], className='three columns'),

        html.Div([
            html.Pre(children="Borough", style={"fontSize": "120%",'font-family':'Arial'}),
            dcc.Checklist(
            id='borough-checklist_location', value=['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND'],
            persistence=True, persistence_type='memory',
            options=[{'label': x.title(), 'value': x} for x in df.BOROUGH.unique()]
        )], className='five columns'),
    ], className='row'),

    dcc.Graph(id='collision_location', figure={}),
    html.Label("Top 10 Dangerous Streets",style={"fontSize": "130%",'font-family':'Arial',"textAlign": "center"}),
    html.Br(),
    html.Div(id='table')
])

@app.callback(
    Output(component_id='collision_location', component_property='figure'),
    [Input(component_id='year-dropdown_location', component_property='value'),
     Input(component_id='borough-checklist_location', component_property='value')])
def display_value(year_chosen, borough_chosen):
    df_fltrd = df[(df['YEAR']==year_chosen)&(df.BOROUGH.isin(borough_chosen))]
    fig = px.scatter_mapbox(df_fltrd,
                            title="Vehicle Collision Distribution in NYC Different Boroughs",
                            lat="LATITUDE",
                            lon="LONGITUDE",
                            color="BOROUGH",
                            zoom=9.24,
                            center=dict(lat=df['LATITUDE'].mean(),
                                        lon=df['LONGITUDE'].mean()))

    fig.update_layout(mapbox_style="open-street-map",title_x=0.5)
    return fig

@app.callback(
    Output(component_id='table', component_property='children'),
    [Input(component_id='year-dropdown_location', component_property='value'),
     Input(component_id='borough-checklist_location', component_property='value')])
def display_value(year_chosen, borough_chosen):
    df_fltrd = df[(df['YEAR']==year_chosen)&(df.BOROUGH.isin(borough_chosen))]
    street=df_fltrd.groupby(['ON STREET NAME','BOROUGH'], as_index=False).size()
    street=street.sort_values(by=['size'],ascending=False).head(10)
    street=street.rename(columns = {'size':'# of Vehicle Collisions'})
    data=street.to_dict('rows')
    columns=[{"name": i, "id": i,} for i in (street.columns)]

    return dash_table.DataTable(data=data, columns=columns)




'''
fig = px.scatter_mapbox(df,
                        lat="LATITUDE",
                        lon="LONGITUDE",
                        color="BOROUGH",
                        zoom=10,
                        center=dict(lat=df['LATITUDE'].mean(),
                                    lon=df['LONGITUDE'].mean()))

fig.update_layout(mapbox_style="open-street-map")

#fig.update_geos(fitbounds="locations")


fig.show()
'''
