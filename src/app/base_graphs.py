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
        size_max=35,
        color='avg_over_par',
        color_continuous_scale='RdYlGn_r',
        center={
            'lat': 51.26,
            'lon': 0.65},
        zoom=8.5,
        hover_name='course',
        hover_data={
            'number_of_rounds': True,
            'par': True,
            'avg_score': True,
            'avg_over_par': True,
            'best_score': True,
            'course_index': True,
            'slope_rating': True,
            'latitude': False,
            'longitude': False,
            },
        labels={
            'number_of_rounds': 'Rounds Played',
            'avg_over_par': 'Average Score Over Par',
            'avg_score': 'Average Score',
            'course_index': 'Course Index',
            'slope_rating': 'Slope Rating',        
            }
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

    fig.update_coloraxes(
        colorbar=dict(
            title=dict(text='<b>Average Score<br>Over Par</b>',
            ),
            x=1.02,
            ticks="outside"
        )
    )

    fig.add_annotation(
        text="○ Circle size denotes number of rounds",
        xref="paper", yref="paper",
        x=0.02, y=0.05,        # Positions it in the bottom left
        showarrow=False,
        font=dict(size=12, color="black"),
        bgcolor="lightgrey",
        bordercolor="gray",
        borderwidth=1,
        borderpad=4,
        opacity=0.8
    )

    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{hovertext}</b>",
            "Rounds Played: %{customdata[0]}",
            "Par: %{customdata[1]}",
            "Avg Score: %{customdata[2]:.1f}",
            "Avg Over Par: %{customdata[3]:.1f}",
            "Best Score: %{customdata[4]}",
            "Course Index: %{customdata[5]}",
            "Slope Rating: %{customdata[6]}",
        ])
    )

    fig.update_layout(
        map_style="carto-voyager-nolabels",
        scattermode='group')    # Prevent points from overlapping

    return fig
