import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

'''
Helper functions for plotly visualizations
'''

def plot_levels(data, by='categories'):
    '''
    Plot Distribution by Level

    Keyword Arguments:
    ------------------
    * data - expanded data from with each level as a column
    * by - distribution of categories or products by level

    Returns:
    --------
    Plotly bar graph
    '''

    if by == 'categories':
        data = data.iloc[:,-6:].apply(pd.Series.nunique)
        title = 'Number of Categories by Level'
    elif by == 'products':
        data =  data.iloc[:,-6:].apply(pd.Series.count)
        title = 'Number of Products by Level'

    x = data[::-1]
    y = data.index[::-1]

    fig = go.Figure(data=go.Bar(x=x,
                            y=y,
                            text=x,
                            textposition='auto',
                            textfont = dict(color='white'),
                            orientation='h',
                           marker_color='rgb(255,103,31)',
                               opacity=0.7),
               layout = go.Layout(
                        title=title)
               )

    fig.show()
