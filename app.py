import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from plot_play import load_data, plot_play


app = Dash(__name__)
server = app.server

################################################################################################
# Data

df = pd.read_csv("./data/plays.csv")
# print(df[:5])
# plays = [{"label": str(playId), "value": playId} for playId in df['playId'].unique()]
games = [{"label": str(gameId), "value": gameId} for gameId in df['gameId'].unique()]
random_gameid = np.random.choice(df['gameId'].unique())
random_playid = np.random.choice(df[df['gameId'] == random_gameid]['playId'].unique())
random_team = df[(df['gameId'] == random_gameid) & (df['playId'] == random_playid)]['possessionTeam'].iloc[0]

# Game State



################################################################################################
# App layout
app.layout = html.Div([

    html.H1("Computer Chair QB", style={'text-align': 'center'}),

    # Menu
    html.Div([
        
        # Selection Div
        html.Div([
        dcc.RadioItems(
            id='select_by',
            options=['Team', 'Week'], 
            value='Team', 
            inline=True,
            style={'width': '100%'}
            ),

        html.P("Select Game:", style={'width': '99%'}),
        html.P("Select Play:", style={'width': '99%'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'width': '100%'}
        ),

        html.Div([
            dcc.Dropdown(
                id='primary_dropdown',
                options=[], 
                value=random_team,
                multi=False,
                style={'width': '99%'},
                searchable=False
                ),

            dcc.Dropdown(
                id='select_game', 
                options=[],
                value=random_gameid,
                multi=False,
                style={'width': "99%"},
                searchable=False
                ),

            dcc.Dropdown(id='select_play',
                multi=False,
                options=[],
                value=random_playid,
                style={'width': "99%"},
                searchable=False
                ),
    ], style={'display': 'flex', 'flex-direction': 'row', 'width': '100%'}),
    
    ], style={'display': 'flex', 'flex-direction': 'column', 'width':'100%'}),

    html.Div([
    # Graph
    dcc.Graph(id='graph_play', config={'displayModeBar':False,'queueLength':0}, figure={}, style={'width': '100%', 'height': '72vh', 'align': 'center'}),
    ], ),

    # Graph Size
    html.Div([        
            html.P("Adjust field width:"),
            dcc.Slider(id='slider', min=25, max=100, step=25, value=100,
                marks={x: str(x) for x in [25, 50, 75, 100]})

        ], style={'display': 'flex', 'flex-direction': 'column', 'width':'100%'})

])


################################################################################################
# Update Graph
@app.callback(
    Output(component_id='graph_play', component_property='figure'),
    [Input(component_id='select_play', component_property='value'),
     Input(component_id='select_game', component_property='value'),
    ]
)
def update_graph(playId, gameId):

    week = df[df['gameId'] == gameId]['week'].iloc[0]

    print(week)
    print(gameId)
    
    if int(playId) != 0:
        fig = plot_play(gameId, playId, load_data(week=week, game=gameId))
    else:
        fig = px.scatter()

    return fig


################################################################################################
# Update Dropdowns

# Populate Primary Dropdown
@app.callback(
    Output(component_id='primary_dropdown', component_property='options'), 
    Input(component_id='select_by', component_property='value')   
)
def update_primary(fltr):
    if fltr == 'Team':
        _ = sorted(df['possessionTeam'].unique())
        return _ 
    else:
        _ = sorted(df['week'].unique())
        return _


# Populate Game Dropdown
@app.callback(
    Output(component_id='select_game', component_property='options'), 
    [Input(component_id='select_by', component_property='value'),
     Input(component_id='primary_dropdown', component_property='value')]
)
def update_games(fltr, optns):
    
    if fltr == 'Team':
        fltr = 'possessionTeam'
    else:
        fltr = 'week'
    
    games = sorted(df[df[fltr] == optns]['gameId'].unique())
    return games


# Populate Play Dropdown
@app.callback(
    Output(component_id='select_play', component_property='options'), 
    Input(component_id='select_game', component_property='value')
)
def update_plays(optns):
    plays = sorted(df[df['gameId'] == optns]['playId'].unique())
    return plays


# Graph Slider
@app.callback(
    Output(component_id='graph_play', component_property='style'), 
    Input(component_id='slider', component_property='value'),   
)
def update_graph_size(width=100):
    return {'width': f'{width}%', 'height': '72vh', 'align': 'center'}


################################################################################################
# Launch App Locally

if __name__ == '__main__':
    app.run_server(debug=True)
