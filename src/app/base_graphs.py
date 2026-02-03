'''
Base graph functions for 
'''

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

def map_golf_courses(df: pd.DataFrame) -> Figure:

    """
    Docstring for map_golf_courses
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: Figure
    """

    fig = px.scatter_map(
        df,
        lat='latitude',
        lon='longitude',
        text='course',
        size='number_of_rounds',
        color='avg_over_par',
        center={
            'lat': 51.26,
            'lon': 0.65},
        zoom=9,
        )

    fig.update_layout()

    # Update trace to position text
    fig.update_traces(
        textposition='bottom right',
        mode='markers+text',
        textfont=dict(
            size=12,
                ),
    )

    fig.update_layout(
        map_style="carto-voyager-nolabels",
        scattermode='group')    # Prevent points from overlapping

    return fig
