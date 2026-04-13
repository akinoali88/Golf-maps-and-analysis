'''
Render 2nd page
'''

# from io import StringIO
# from dash import dcc, html, callback, Input, Output
# from dash.exceptions import PreventUpdate
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
from src.app.dashboard_logic import create_page_header
from src.app.base_graphs import plot_score_over_time


def render_page2(df: pd.DataFrame) -> dbc.Container:

    """
    Constructs the 'Performance History' layout for the dashboard.

    This page focuses on the longitudinal analysis of golf scores, providing 
    a visual timeline of golf scores since 2016.

    Args:
        df (pd.DataFrame): The validated golf dataset containing date-indexed 
            scoring data required for time-series plotting.
        
    Returns:
        dbc.Container: A fluid Bootstrap container comprising:
            - A standardized page header with performance-themed iconography.
            - An interactive time-series line chart (dcc.Graph) showing score 
              trends over the years.
            
    Notes:
        The layout utilizes Dash Bootstrap Components (DBC) for a responsive 
        grid system. The 'score-over-time' graph is initialized here but can 
        be further manipulated via Dash callbacks using its component ID.
    """


    initial_fig = plot_score_over_time(df)

    return dbc.Container([

            # Header Section
            create_page_header(
                    header_title='Performance History',
                    subtitle='Breakdown of scores and performance details over time',
                    footer_text='Based on rounds completed since 2016',
                    icon_class='card-list'),

            # Performance chart over time
            dbc.Card([
                dbc.CardBody(
                    dcc.Graph(
                        id="score-over-time",
                        figure=initial_fig,
                        config={"displayModeBar": False},
                        style={"height": "500px", "marginTop": "-2.5px"},
                        ),
                    ),
            ], className="py-2 px-3"),

            # Detail breakdown
            ], fluid=True) # Close Container
