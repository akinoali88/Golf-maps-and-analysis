"""
Generated Dash application factory module.
Includes functions to create Plotly figures and initialize the Dash app.
"""

from dash import Dash, dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
from src.app.components import render_home_tab, render_page2, render_page3


def create_dash_app(course_df: pd.DataFrame,
                    round_df: pd.DataFrame
                    ) -> Dash:
    """
    Initializes and configures the Dash application for golf performance analysis.

    This factory function sets up the Dash instance, applies Bootstrap theming, 
    and constructs a multi-tab layout. Data is serialized to JSON and stored 
    client-side in dcc.Store components to facilitate interactive filtering.

    Args:
        course_df (pd.DataFrame): Geospatial and metadata for golf courses 
            (e.g., coordinates, course names).
        round_df (pd.DataFrame): Historical round data, including scores, 
            dates, and performance metrics per course.

    Returns:
        Dash: A configured Dash application object ready to be run via .run_server().

    Notes:
        - The app uses the 'spacelab' Bootstrap theme for consistent styling.
        - Tab 1: 'Location Maps' renders geospatial visualizations of courses.
        - Tab 2: 'Performance History' displays statistical trends over time.
        - Tab 3: 'Course Metrics' provides granular breakdown of play data. 
    """

    # load bootstrap figure templates
    dbc_theme = "spacelab"

    load_figure_template(dbc_theme)
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

    app = Dash(__name__,
               external_stylesheets=[dbc.themes.SPACELAB, dbc_css, dbc.icons.BOOTSTRAP]
               )

    # Define the app layout
    app.layout = dbc.Container([

            # Store the data as JSON in the browser/app state
            dcc.Store(id="main-data", data=course_df.to_json(orient="records")),
            dcc.Store(id="round-data", data=round_df.to_json(orient="records")),

            dbc.Tabs([

                # --- Home page tab ---
                dbc.Tab([
                    render_home_tab(course_df)],
                    label="Location Maps",
                    label_class_name="bg-primary-subtle text-grey",
                    ),

                # --- Course History ---
                dbc.Tab([
                    render_page2(round_df)],
                    label="Performance History",
                    label_class_name="bg-primary-subtle text-grey",
                    ),

                # --- etc ---
                dbc.Tab([
                    render_page3()],
                    label="Course Metrics",
                    label_class_name="bg-primary-subtle text-grey",
                        ),
                    ]) # Close dcc.Tabs
        ],
        fluid=True,
        className="bg-primary",
        style={"minHeight": "100vh"}) # Close dbc.Container

    return app
