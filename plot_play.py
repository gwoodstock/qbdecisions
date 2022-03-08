import plotly.express as px
import pandas as pd

def load_data(week=0, team=0, game=0):

    data = pd.read_csv('./data/test_plays.csv')

    return data
    

def plot_play(gameId, playId, data):

    data_graph = data[
        (data['gameId'] == gameId) &
        (data['playId'] == playId)    
        ].copy()
    data_graph.reset_index(drop=True, inplace=True)

# print out
    print(f'Game ID: {data_graph["gameId"].loc[0]}\nPlay: {data_graph["playId"].loc[0]}')
    
    # build play
    fig = px.scatter(data_frame=data_graph, x='x', y='y', hover_name='displayName', hover_data=['team', 'position'], range_x=[0, 120], range_y=[0, 53], animation_frame='frameId',
                     color='team', color_discrete_sequence=['#B90E0A', '#1338BE', '#80471C'], # red, blue, brown
                     symbol = 'team', symbol_sequence = ['circle', 'x', 'diamond-wide'])

    # style field
    # field         
    fig.add_vline(x=10, line_color='#FFFFFF')   # end zone line left
    fig.add_vline(x=110, line_color='#FFFFFF')  # end zone line right
    fig.update_yaxes(gridcolor='#327c09')   # yard lines
    fig.update_xaxes(gridcolor='#FFFFFF')   # yard lines        # https://plotly.com/python/reference/layout/xaxis/#layout-xaxis-gridcolor
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110],
            ticktext = ['Goal', '10', '20', '30', '40', '50', '40', '30', '20', '10', 'Goal']),
        yaxis = dict(
            tickmode = 'array',
            tickvals = [],
            ticktext = [])
    )   # https://plotly.com/python/tick-formatting/
    fig.update_layout(plot_bgcolor='#327c09')   # field color   # https://plotly.com/python/reference/layout/#layout-plot_bgcolor

    # style marker
    fig.update_traces(marker=dict(  size=24,
                                    line=dict(width=2,
                                    color='DarkSlateGrey')),
                      selector=dict(mode='markers'))    # https://plotly.com/python/marker-style/
    
    # animation
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 100 # frame rate

    return fig


if __name__ == '__main__':
    pass