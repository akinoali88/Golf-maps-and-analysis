'''
Generated Dash application factory module.
Includes functions to create Plotly figures and initialize the Dash app.
'''

from dash import Dash #,  dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
from src.app.components import render_home_tab, render_page2, render_page3


def create_dash_app(df: pd.DataFrame) -> Dash:
    '''
    Create and configure a Dash application for baby feeding schedule visualization.

    Parameters:    
        df : pd.DataFrame
            insert details


    Returns:
        Dash
            Configured Dash application instance with interactive layout, callbacks, and graphs.

    Notes:
        - Home page contains a map of all courses played at
        - A second page showing invidivudal stats by course over time
    '''

    # load bootstrap figure templates
    dbc_theme = 'minty'

    load_figure_template(dbc_theme)
    dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css'

    app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc_css, dbc.icons.BOOTSTRAP])

    # Define the app layout
    app.layout = dbc.Container([

            # Store the data as JSON in the browser/app state
#            dcc.Store(id='main-data', data=df.to_json(orient='records')),

            dbc.Tabs([

                # --- Home page tab ---
                dbc.Tab([
                    render_home_tab(df)],
                    label='Location Maps',
                    label_class_name='bg-primary-subtle text-grey',
                    ),

                # --- Course History ---
                dbc.Tab([
                    render_page2()],
                    label='Performance',
                    label_class_name='bg-primary-subtle text-grey',
                    ),

                # --- etc ---
                dbc.Tab([
                    render_page3()],
                    label='Course History',
                    label_class_name='bg-primary-subtle text-grey',
                        ),
                    ]) # Close dcc.Tabs
        ],
        fluid=True,
        className='bg-success',
        style={'minHeight': '100vh'}) # Close dbc.Container

    return app
