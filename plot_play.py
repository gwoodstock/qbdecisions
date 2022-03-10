import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def load_data(week=0, team=0, game=0):

    data = pd.read_csv(f'./data/raw/week {week}/{game}.csv', compression='zip')

    return data


def get_play_state():
    data = pd.read_csv('./data/plays.csv')

    return data


    

def plot_play(gameId, playId, data):

    team_map = {
        'color': {
    'ARI':	['#97233F', '#000000'],
    'ATL':	['#A71930', '#000000'],
    'BAL':	['#241773', '#000000'],
    'BUF':	['#00338D', '#C60C30'],
    'CAR':	['#0085CA',	'#101820'],
    'CHI':	['#0B162A',	'#C83803'],
    'CIN':	['#FB4F14',	'#000000'],
    'CLE':	['#311D00',	'#FF3C00'],
    'DAL':	['#003594',	'#041E42'],
    'DEN':	['#FB4F14',	'#002244'],
    'DET':	['#0076B6',	'#B0B7BC'],
    'GB':	['#FFB612', '#203731'],
    'HOU':	['#03202F',	'#A71930'],
    'IND':	['#002C5F',	'#A2AAAD'],
    'JAX':	['#101820',	'#D7A22A'],
    'KC':	['#E31837',	'#FFB81C'],
    'LA':	['#003594',	'#FFA300'],
    'LAC':	['#0080C6',	'#FFC20E'],
    'MIA':	['#008E97',	'#FC4C02'],
    'MIN':	['#4F2683',	'#FFC62F'],
    'NE':	['#002244', '#C60C30'],
    'NO':	['#D3BC8D',	'#101820'],
    'NYG':	['#0B2265',	'#A71930'],
    'NYJ':	['#125740',	'#000000'],
    'OAK':	['#000000',	'#A5ACAF'],
    'PHI':	['#004C54',	'#A5ACAF'],
    'PIT':	['#FFB612',	'#101820'],
    'SEA':	['#002244',	'#69BE28'],
    'SF':	['#AA0000',	'#B3995D'],
    'TB':	['#D50A0A',	'#FF7900'],
    'TEN':	['#0C2340',	'#4B92DB'],
    'WAS':	['#5A1414',	'#FFB612']
        },
        'full_name': {
    'ARI':	'Cardinals',
    'ATL':	'Falcons',
    'BAL':	'Ravens',
    'BUF':	'Bills',
    'CAR':	'Panthers',
    'CHI':	'Bears',
    'CIN':	'Bengals',
    'CLE':	'Browns',
    'DAL':	'Cowboys',
    'DEN':	'Broncos',
    'DET':	'Lions',
    'GB':	'Packers',
    'HOU':	'Texans',
    'IND':	'Colts',
    'JAX':	'Jaguars',
    'KC':	'Chiefs',
    'LA':	'Rams',
    'LAC':	'Chargers',
    'MIA':	'Dolphins',
    'MIN':	'Vikings',
    'NE':	'Patriots',
    'NO':	'Saints',
    'NYG':	'Giants',
    'NYJ':	'Jets',
    'OAK':	'Raiders',
    'PHI':	'Eagles',
    'PIT':	'Steelers',
    'SEA':	'Seahawks',
    'SF':	'49ers',
    'TB':	'Buccanneers',
    'TEN':	'Titans',
    'WAS':	'Washington',
    'football': 'Football',
    np.nan: np.nan
        }
    }
    
    data_graph = data[
        (data['gameId'] == gameId) &
        (data['playId'] == playId)    
        ].copy()
    data_graph.reset_index(drop=True, inplace=True)
    data_graph['team'] = data_graph['team'].astype(pd.CategoricalDtype(categories=['home', 'away', 'football'], ordered=True))
    data_graph.sort_values(by=['frameId', 'team'], inplace=True)
    
    try:
        home_team = data_graph[data_graph['team'] == 'home'].iloc[0]['team_name']
        away_team = data_graph[data_graph['team'] == 'away'].iloc[0]['team_name']
        data_graph['team'] = data_graph['team'].str.replace('football', 'Football')

        home_name = team_map['full_name'][home_team]
        away_name = team_map['full_name'][away_team]

        pos_team = data_graph[data_graph['possession'] == 1]['team_name'].iloc[0]
        pos_team = team_map['full_name'][pos_team]
        
        def_team = data_graph[data_graph['possession'] == 0]['team_name'].iloc[0]
        def_team = team_map['full_name'][def_team]
        
        home_c1 = team_map['color'][home_team][0]
        home_c2 = team_map['color'][home_team][1]
        away_c1 = team_map['color'][away_team][0]
        away_c2 = team_map['color'][away_team][1]
    except Exception as e:
        home_team = ''
        away_team = ''

        home_name = ''
        away_name = ''

        pos_team = ''
        
        def_team = ''
        
        home_c1 = ''
        home_c2 = ''
        away_c1 = ''
        away_c2 = ''

    # play state
    play_state = get_play_state()
    play_state = play_state[(play_state['gameId'] == gameId) & (play_state['playId'] == playId)]
    if(play_state.shape[0] > 0):
        los = play_state['absoluteYardlineNumber'].iloc[0]
        ytg = los - play_state['yardsToGo'].iloc[0]
    else:
        los = 50
        ytg = 60



    # print out
    print(f'Game ID: {data_graph["gameId"].loc[0]}\nPlay: {data_graph["playId"].loc[0]}')
    
    # build play
    fig = px.scatter(data_frame=data_graph, x='y', y='x', hover_name='displayName', hover_data=['team', 'position'], range_y=[120, 0], range_x=[0, 53], animation_frame='frameId',
                     color='team', color_discrete_sequence=[home_c1, away_c1, '#80471C'], # red, blue, brown
                     symbol = 'team', symbol_sequence = ['circle', 'x', 'diamond-tall'])#.update_layout(title_x=0.01)
    
    fig.update_layout(#title_x=0.5,
                        yaxis={'title':{'text':None}, 'fixedrange':True},
                        xaxis={'title':{'text':None}, 'fixedrange':True})
    
    fig.add_annotation(text='',
                  xref="paper", yref="paper",
                  x=.5, y=1, showarrow=False,
                  font=dict(size=30, color=home_c1)
                  )

    if los > 10:
        fig.add_annotation(text='Touchdown',
                    xref="paper", yref="paper",
                    x=.5, y=1, showarrow=False,
                    font=dict(size=30, color=home_c2)
                    )
    fig.add_hrect(y0=0, y1=10, line_width=0, fillcolor=home_c1, opacity=0.25)
    
    fig.add_annotation(text='Touchdown',
                  xref="paper", yref="paper",
                  x=.5, y=0, showarrow=False,
                  font=dict(size=30, color=home_c2)
    )
    fig.add_hrect(y0=110, y1=120, line_width=0, fillcolor=home_c1, opacity=0.25)

    


    # style field
    fig.add_hline(y=10, line_color='#FFFFFF')                                       # end zone line left
    fig.add_hline(y=110, line_color='#FFFFFF')                                      # end zone line right
    fig.add_hline(y=los, line_color='DarkSlateGrey', line_dash="dash")              # LOS
    fig.add_hline(y=ytg, line_color='yellow')                                       # Line to gain

    fig.update_layout(
            yaxis = dict(
                tickmode = 'array',
                tickvals = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110],
                ticktext = ['Goal', '10', '20', '30', '40', '50', '40', '30', '20', '10', 'Goal']
                ),
            xaxis = dict(
                tickmode = 'array',
                tickvals = [],
                ticktext = []
                ),
            plot_bgcolor='#327c09',
            yaxis_range=[120, 0],
            xaxis_range=[0, 53.3],
            legend = {
                'title': '',
                'font_size': 24
            }
    )
       
    # style marker
    fig.update_traces(marker=dict(
                                size=24,
                                line=dict(
                                    width=2,
                                    # color=home_c2
                                    )
                                ),
                      selector=dict(
                                mode='markers'
                                )
                                )
    
    # print(fig['data'])
    fig['data'][0]['marker']['line']['color'] = home_c2     # home team border
    fig['data'][1]['marker']['line']['color'] = away_c2     # away team border
    fig['data'][2]['marker']['line']['color'] = '#80471C'   # football border
    fig['data'][0]['name'] = home_name
    fig['data'][1]['name'] = away_name

    # # animation
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 100 # frame rate
    
    for button in fig.layout.updatemenus[0].buttons:
        button['args'][1]['frame']['redraw'] = True

    event_delay = ''
    for k in range(len(fig.frames)):
        # print(fig.frames[k])
        fig.frames[k]['data'][0]['name'] = home_name
        fig.frames[k]['data'][1]['name'] = away_name

        # fig.frames[k]['layout'].update(title_text=f'My title {k}')
        # fig.frames[k]['layout'].update(legend={'title': {'text':f'My title {k}'}, 'tracegroupgap': 0})

        # animate event annotations
        f = sorted(data_graph['frameId'].unique())
        event = data_graph[data_graph['frameId'] == f[k]]['event'].iloc[0]
        event = event.replace('_', ' ').title()
        if event != 'None': # update fresh event
            event_delay = event
            fig.frames[k]['layout'].update(annotations=
                [{'font': {'color': '#203731', 'size': 30},
                        'showarrow': False,
                        'text': event,
                        'x': 0.5,
                        'xref': 'paper',
                        'y': .5,
                        'yref': 'paper'
                    }])
        else:   # update with last event != None
            fig.frames[k]['layout'].update(annotations=
                [{'font': {'color': '#203731', 'size': 30},
                        'showarrow': False,
                        'text': event_delay,
                        'x': 0.5,
                        'xref': 'paper',
                        'y': .5,
                        'yref': 'paper'
                 }])

    return fig


if __name__ == '__main__':
    pass