'''
Render 2nd page
'''

# from io import StringIO
# from dash import dcc, html, callback, Input, Output
# from dash.exceptions import PreventUpdate
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from src.app.dashboard_logic import create_page_header


def render_page2(df: pd.DataFrame) -> dbc.Container:

    """
    This function constructs the layout for

    Parameters:
        df: pd.DataFrame
            DataFrame containing 
        
    Returns:
        dbc.Container
            A Bootstrap container component containing the complete home tab layout with:
            - a
            - b 
            
    Notes:
        The component uses Dash Bootstrap Components for responsive layout and
        styling. Chart interactions and statistics updates are handled via Dash callbacks
        using the component IDs defined in this function.

    """


    initial_fig = px.scatter(df,
                             x="date",
                             y="over_par",
                             trendline='rolling',
                             trendline_options=dict(window=5),
                             title='Score over par over time')

    return dbc.Container([

            # Header Section
            create_page_header(
                    header_title='Performance History',
                    subtitle='Breakdown of scores and performance details over time',
                    footer_text='Based on rounds completed since 2016',
                    icon_class='card-list'),

            # Performance chart over time
            dcc.Graph(
                id="score-over-time",
                figure=initial_fig,
                config={"displayModeBar": False},
                style={"height": "500px", "marginTop": "-2.5px"},
                ),

            # Deteail breakdown
            'Some charts showing performance over time....'
            ], fluid=True) # Close Container

# @callback(
#     )
# def update_individual_violin(args):

#     '''Input callback to update '''

#     return
