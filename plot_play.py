import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def load_data(week=0, team=0, game=0):

    # data = pd.read_csv(f'./data/raw/week {week}/{game}.csv', compression='zip')
    data = pd.read_csv(f'./data/pred/week_{week}.csv', compression='zip')
    data = data[data['gameId'] == game].copy()

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
    data_graph['team'] = data_graph['team'].astype(pd.CategoricalDtype(categories=['home', 'away', 'football', 'Optimal Receiver'], ordered=True))
    data_graph.sort_values(by=['frameId', 'team'], inplace=True)
    
    # print(data_graph[data_graph['team'] == 'away'].iloc[0]['team_name'])

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

        
        # # estimated epa
        # est_epa = data_graph['est_epa']
        # print(est_epa)

        # # estimated completion percentage
        # est_comp = data_graph['preds']
        # print(est_comp)

        # # optimal rec
        
        # print(optimal_rec)
        # # actual epa gained

        # # adjusted epa
        # adjusted_epa = data_graph[data_graph['displayName'] == optimal_rec]['optimal_epa'].max()
        # print(adjusted_epa)

        # # epa over optimal
        # epa_over_optimal = actual_epa - adjusted_epa
        # print(epa_over_optimal)


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

        los = data_graph[data_graph['team'] == 'Football'].iloc[0]['x']
        ytg = los - play_state['yardsToGo'].iloc[0]
        score_home = play_state['preSnapHomeScore'].iloc[0]
        score_away = play_state['preSnapVisitorScore'].iloc[0]
        clock = play_state['gameClock'].iloc[0]
        down = int(data_graph[data_graph['down'].notna()]['down'].iloc[0])
        quarter = play_state['quarter'].iloc[0]
        desc = play_state['playDescription'].iloc[0]
    else:
        los = 50
        ytg = 60
        score_home = 0
        score_away = 0
        clock = ''
        down = 1
        quarter = 1
        desc = ''

    try:
        optimal_rec = data_graph[data_graph['optimal_receiver'].notna()]['optimal_receiver'].iloc[0]
        actual_epa = np.round(data_graph[data_graph['epa_actual'].notna()]['epa_actual'].iloc[0], 1)
        optimal_epa = np.round(data_graph[data_graph['displayName'] == optimal_rec]['optimal_epa'].max(), 1)
    except Exception as e:
        print('No opt rec')

    if optimal_rec in list(data_graph['displayName'].unique()):
        data_graph.loc[(data_graph['displayName'] == optimal_rec), 'team'] = 'Optimal Receiver'
        data_graph['team'] = data_graph['team'].astype(pd.CategoricalDtype(categories=['home', 'away', 'Football', 'Optimal Receiver'], ordered=True))
        data_graph.sort_values(by=['frameId', 'team'], inplace=True)        

    data_graph['preds'] = np.round(data_graph['preds'] * 100, 1)
    data_graph['est_epa'] = np.round(data_graph['est_epa'], 1)    
    
    data_graph['preds'].fillna(0, inplace=True)
    data_graph['preds'] = data_graph['preds'].astype(str)
    data_graph['preds'] = data_graph['preds'].replace('0.0', ' ')

    data_graph['est_epa'].fillna(100, inplace=True)
    data_graph['est_epa'] = data_graph['est_epa'].astype(str)
    data_graph['est_epa'] = data_graph['est_epa'].replace('100.0', ' ')

    qbiq = 0
    if actual_epa > optimal_epa > 0:
        qbiq += 1
    if actual_epa < optimal_epa < 0 and actual_epa > 0:
        qbiq += .5
    
    qbiq = np.round(1 + qbiq * actual_epa, 1)

    # print out
    print(f'Game ID: {data_graph["gameId"].loc[0]}\nPlay: {data_graph["playId"].loc[0]}')

    # build play
    fig = px.scatter(data_frame=data_graph, x='y', y='x', range_y=[120, 0], range_x=[0, 53], animation_frame='frameId',
                     color='team', color_discrete_sequence=[home_c1, away_c1, '#80471C', '#FFD700'], # red, blue, brown, gold
                     symbol = 'team', symbol_sequence = ['circle', 'x', 'diamond-tall', 'star'], custom_data=['displayName', 'preds', 'est_epa', 'position'])#.update_layout(title_x=0.01)       , 'star'

    fig.update_traces(
    hovertemplate="<br>".join([
        "<b> %{customdata[0]}</b> %{customdata[3]}",
        "Catch Prob: %{customdata[1]}%",
        "Est. EPA: %{customdata[2]}"]))

    fig.update_layout(#title_x=0.5,
                        yaxis={'title':{'text':None}, 'fixedrange':True},
                        xaxis={'title':{'text':None}, 'fixedrange':True})
    
    fig.add_annotation(text='',
                  xref="paper", yref="paper",
                  x=.5, y=1, showarrow=False,
                  font=dict(size=30, color=home_c1)
                  )
    if optimal_epa > 0:
        opt_sign = '+'
    else:
        opt_sign = ''
    if actual_epa > 0:
        act_sign = '+'
    else:
        act_sign = ''
    if qbiq > 0:
        qb_sign = '+'
    else:
        qb_sign = ''
    
    fig.add_annotation(text=f'QB-iQ {qb_sign}{qbiq}<br>Optimal EPA {opt_sign}{optimal_epa} | Actual EPA: {act_sign}{actual_epa}',
                     xref="paper", yref="paper", yanchor='bottom', xanchor='right',
                     x=1., y=1., showarrow=False,
                     font=dict(size=18, color='black')
                        )

    if down == 1:
        ending = 'st'
    if down == 2:
        ending = 'nd'
    if down == 3:
        ending = 'rd'
    if down == 4:
        ending = 'th'
    to_go = int((los - ytg))
    fig.add_annotation(text=f'{down}{ending} & {to_go}',
                     xref="paper", yref="y", yanchor='top', xanchor='right',
                     x=1., y=los, showarrow=False,
                     font=dict(size=18, color='white')
                        )
    fig.add_hrect(y0=0, y1=10, line_width=0, fillcolor=home_c1, opacity=0.3)
    
    # fig.add_annotation(text='Touchdown',
    #               xref="paper", yref="paper",
    #               x=.5, y=0, showarrow=False,
    #               font=dict(size=30, color=home_c2)
    # )
    fig.add_hrect(y0=110, y1=120, line_width=0, fillcolor=home_c1, opacity=0.3)

    _ = 100
    _ += ~desc[_:0:-1].index(' ') + 1
    
    desc = desc[:_] + '<br>' + desc[_:] # split long strings into 2 or 3 lines on the last space before 100th char
    fig.add_annotation(text=desc,
                  xref="paper", yref="paper",
                  x=.5, y=0, showarrow=False,
                  yanchor='top',
                  font=dict(size=16)
    )
    


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
    
    # # opEPA vs Actual EPA
    # optimal_epa_idx = data_graph['epa_est'].idxmax()
    # optimal_epa = data_graph.loc[optimal_epa_idx, 'epa_est'].iloc[0]
    # actual_epa = data_graph['epa'].iloc[0]
    # epa_delta = actual_epa - optimal_epa
    
    # # Optimal Target
    # optimal_receiver = data_graph.loc[optimal_epa_idx, 'displayName'].iloc[0]

    # # Play Success
    # play_success = 0
    # if epa_delta > 0:
    #     play_success = 1
    # elif epa_delta <= 0 and actual_epa > 0:
    #     play_success = .5




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
        
        fig.frames[k]['data'][0]['name'] = home_name
        fig.frames[k]['data'][1]['name'] = away_name

        # Hover Data
        fig.frames[k]['data'][0]['hovertemplate'] = "<br>".join([
        "<b> %{customdata[0]}</b> %{customdata[3]}",
        "Catch Prob: %{customdata[1]}%",
        "Est. EPA: %{customdata[2]}"])
        fig.frames[k]['data'][1]['hovertemplate'] = "<br>".join([
        "<b> %{customdata[0]}</b> %{customdata[3]}",
        "Catch Prob: %{customdata[1]}%",
        "Est. EPA: %{customdata[2]}"])
        fig.frames[k]['data'][2]['hovertemplate'] = "Football"
        fig.frames[k]['data'][3]['hovertemplate'] = "<br>".join([
        "<b> %{customdata[0]}</b> %{customdata[3]}",
        "Catch Prob: %{customdata[1]}%",
        "Est. EPA: %{customdata[2]}"])

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
                        'yanchor': 'bottom',
                        'x': 0.5,
                        'xref': 'paper',
                        'y': 1,
                        'yref': 'paper'
                    }])
        else:   # update with last event != None
            fig.frames[k]['layout'].update(annotations=
                [{'font': {'color': '#203731', 'size': 30},
                        'showarrow': False,
                        'text': event_delay,
                        'yanchor': 'bottom',
                        'x': 0.5,
                        'xref': 'paper',
                        'y': 1,
                        'yref': 'paper'
                 }])

    return fig, home_name, int(score_home), away_name, int(score_away)


if __name__ == '__main__':
    pass