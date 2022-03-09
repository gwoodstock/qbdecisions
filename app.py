import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from plot_play import load_data, plot_play


app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)

df = pd.read_csv("./data/test_plays.csv")
# print(df[:5])
# plays = [{"label": str(playId), "value": playId} for playId in df['playId'].unique()]
games = [{"label": str(gameId), "value": gameId} for gameId in df['gameId'].unique()]


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Professional Football Pass Plays from 2018", style={'text-align': 'center'}),

    # Menu
    html.Div([
        html.Div(children=
        [
            dcc.Dropdown(
                id="select_game", 
                options=games,
                multi=False,
                value=2018090912,
                style={'width': "100%"}
                ),

            dcc.Dropdown(id="select_play",
                multi=False,
                value=3081,
                style={'width': "100%"}
                )
    ], style={'display': 'flex', 'flex-direction': 'row', 'width': '50%'}),

        html.Div([], style={'display': 'flex', 'flex-direction': 'row', 'width':'50%'})    # empty half of row
    
    ])
    ,

    html.Div(id='output_container', children=[]),   # print out

    dcc.Graph(id='graph_play', figure={}, style={'width': '100%', 'height': '80vh'})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='graph_play', component_property='figure')],
    
    [Input(component_id='select_play', component_property='value'),
     Input(component_id='select_game', component_property='value'),
    ]
)
def update_graph(playId, gameId):

    container = f'The year chosen by user was: {playId}'

    # Filtered Data for graphing
    # not currently used

    fig = plot_play(gameId, playId, df)


    return container, fig

@app.callback(
    Output(component_id='select_play', component_property='options'), 
    Input(component_id='select_game', component_property='value'),
    
)
def update_plays(gameId):
    plays = df[df['gameId'] == gameId]['playId'].unique()
    return plays

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
