'''
Render the 3rd page
'''

# from io import StringIO
# from dash import dcc, html, callback, Input, Output
# from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
# import pandas as pd
from src.app.dashboard_logic import create_page_header


def render_page3() -> dbc.Container:

    '''
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

    '''

    return dbc.Container([

            # Header Section
            create_page_header(
                    header_title='Course Detail',
                    subtitle='Breakdown of scores and performance details at specific courses',
                    footer_text='Based on rounds completed since 2016',
                    icon_class='card-list'),


            # Deteail breakdown
            'Some charts showing performance over time....'
            ], fluid=True) # Close Container

# @callback(
#     )
# def update_individual_violin(args):

#     '''Input callback to update '''

#     return
