'''
Base graph functions for 
'''

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

def map_golf_courses(df: pd.DataFrame) -> Figure:

    '''
    Docstring for map_golf_courses
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: Figure
    '''

    fig = px.scatter_map(df,
                         lat='Latitude',
                         lon='Longitude',
                         hover_name='Golf Course',
                         #size = 'tbc'
                            )

    fig.update_layout(scattermode='group')

    return fig
