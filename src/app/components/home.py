'''
Render the home tab for ....
'''

# from io import StringIO

#from dash import dcc, html, callback, Input, Output
# from dash.exceptions import PreventUpdate
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from src.app.dashboard_logic import create_page_header, create_course_badges, get_top_bottom_courses
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

    top_courses = get_top_bottom_courses(df, top=True)
    bottom_courses = get_top_bottom_courses(df, top=False)

    return dbc.Container([
            # Header Section
            create_page_header(
                    header_title="Akin's Golf Dashboard",
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

                            # 2. Top 5 Courses Row
                            create_course_badges(
                                header_title='Top 5 scoring venues (avg vs par)',
                                courses=top_courses,
                                header_colour='success'),

                            # --- BOTTOM 5 ROW ---
                            create_course_badges(
                                header_title='Bottom 5 scoring venues (avg vs par)',
                                courses=bottom_courses,
                                header_colour='warning'),

                            # The Map
                            dcc.Graph(
                                id='maps',
                                figure=initial_fig,
                                config={'displayModeBar': False},
                                style={'height': '550px', 'marginTop': '-10px'},
                                )
                                    ],)
                            ], className='shadow-sm mb-2')
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
