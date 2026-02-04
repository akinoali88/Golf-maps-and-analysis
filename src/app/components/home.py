'''
Render the home tab for ....
'''

# from io import StringIO

#from dash import dcc, html, callback, Input, Output
# from dash.exceptions import PreventUpdate
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from src.app.dashboard_logic import create_page_header
from src.app.base_graphs import map_golf_courses

def render_home_tab(df: pd.DataFrame) -> dbc.Container:

    '''
    This function constructs the main dashboard layout for 

    Parameters:
        df: pd.DataFram
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

    initial_fig = map_golf_courses(df)

    rounds = df['number_of_rounds'].sum()

    return dbc.Container([
            # Header Section
            create_page_header(
                    header_title="Akin's Golf Locations",
                    subtitle=(f'Performance analysis by golf course of {rounds} '
                             'rounds played since 2016'),
                    footer_text='Data tracked and visualized using Python, Dash, and Plotly',
                    icon_class='globe-europe-africa'),

            # Stat Cards
            #'Stat cards',

            # Map golf courses
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            # Title
                            html.H5("Akin's Course Analytics", className='card-title'),

                            # The Map
                            dcc.Graph(
                                id='maps',
                                figure=initial_fig,
                                config={'displayModeBar': False},
                                # 'flex': '1' tells the graph to grow and fill all available space
                                style={'height': '100%', 'flex': '1'}
                            )
                        ],
                        style={
                            "height": "75vh", 
                            "display": "flex", 
                            "flexDirection": "column"
                        })
                    ], className='shadow-sm mb-4')
                ], width=12)
            ])

        ], fluid=True) # Close Container

# Callbacks for home page tab
# @callback(
#     []
# )
# def update_daily_metrics(args):
#     '''Input callback to update

#     '''


#     return
