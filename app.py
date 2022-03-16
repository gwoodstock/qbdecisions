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

games = [{"label": str(gameId), "value": gameId} for gameId in df['gameId'].unique()]
# random_gameid = np.random.choice(df['gameId'].unique())
# random_playid = np.random.choice(df[df['gameId'] == random_gameid]['playId'].unique())
# random_team = df[(df['gameId'] == random_gameid) & (df['playId'] == random_playid)]['possessionTeam'].iloc[0]
random_playid = 75
random_gameid = 2018090600
random_team = 'ATL'

################################################################################################
# App layout
app.layout = html.Div([
    html.B(),

    # Menu
    html.Div([
        # Selection Div
        html.Div([
            html.B(),
            dcc.RadioItems(
                id='select_by',
                options=['Team', 'Week'], 
                value='Team', 
                inline=True,
                style={'width': '90%'}
                ),
            dcc.Dropdown(
                id='primary_dropdown',
                options=[], 
                value=random_team,
                multi=False,
                style={'width': '90%'},
                searchable=False
                ),

            dcc.Dropdown(
                id='select_game', 
                options=[],
                value=random_gameid,
                multi=False,
                style={'width': "90%"},
                searchable=False
                ),

            dcc.Dropdown(
                id='select_play',
                multi=False,
                options=[],
                value=random_playid,
                style={'width': "90%"},
                searchable=False
                ),
    ], style={'display': 'flex', 'flex-direction': 'column', 'width': '80%'}),

        # Scoreboard Div
        html.Div([
            
            html.Div([
                html.P('', style={'width': '25%', 'fontSize': 24, 'align-items': 'center'}),
                html.P(children='', id='home_name', style={'width': '45%', 'fontSize': 24}),
                html.P(children='', id='score_home', style={'width': '5%', 'fontSize': 24}),
                html.P('', style={'width': '25%', 'fontSize': 24, 'align-items': 'right'}),

            ], style={'display': 'flex', 'flex-direction': 'row', 'width': '100%'}),
            
            html.Div([
                html.P('', style={'width': '25%', 'fontSize': 24, 'align-items': 'center'}),
                html.P(children='', id='away_name', style={'width': '45%', 'fontSize': 24}),
                html.P(children='', id='score_away', style={'width': '5%', 'fontSize': 24}),
                html.P('', style={'width': '25%', 'fontSize': 24, 'align-items': 'right'}),

            ], style={'display': 'flex', 'flex-direction': 'row', 'width': '100%'}),

            html.Hr(style={'width': '50%', 'fontSize': 24, 'align-items': 'center'}),


    ], style={'display': 'flex', 'flex-direction': 'column', 'width': '100%', 'align': 'top'}),

        # More Info Div
        html.Div([

            html.H1("QB-iQ", style={'text-align': 'center'}),
            html.P('by Gene Woodstock')

    ], style={'display': 'flex', 'flex-direction': 'column', 'width': '80%', 'align-items': 'center'}),

    ], style={'display': 'flex', 'flex-direction': 'row', 'width':'100%'}),

    html.Div([
    # Graph
    dcc.Graph(id='graph_play', config={'displayModeBar':False,'queueLength':0}, figure={}, style={'width': '100%', 'height': '70vh', 'align': 'center'}),
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
    [Output(component_id='graph_play', component_property='figure'),
     Output(component_id='home_name', component_property='children'),
     Output(component_id='score_home', component_property='children'),
     Output(component_id='away_name', component_property='children'),
     Output(component_id='score_away', component_property='children')],

    [Input(component_id='select_play', component_property='value'),
     Input(component_id='select_game', component_property='value'),
    ]
)
def update_graph(playId, gameId):

    week = df[df['gameId'] == gameId]['week'].iloc[0]

    # print(week)
    # print(gameId)
    
    if int(playId) != 0:
        fig, home_name, score_home, away_name, score_away = plot_play(gameId, playId, load_data(week=week, game=gameId))
    else:
        fig = px.scatter()
        home_name, score_home, away_name, score_away = 0, 0, 0, 0

    return fig, home_name, str(score_home), away_name, str(score_away)


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
    return {'width': f'{width}%', 'height': '70vh', 'align': 'center'}


################################################################################################
# Launch App Locally

if __name__ == '__main__':
    app.run_server(debug=False)
