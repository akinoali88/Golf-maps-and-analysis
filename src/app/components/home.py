'''
Render the home tab for ....
'''

from io import StringIO

# from dash.exceptions import PreventUpdate
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output
from src.app.dashboard_logic import create_page_header, create_course_badges, get_top_bottom_courses
from src.app.base_graphs import map_golf_courses

def render_home_tab(df: pd.DataFrame) -> dbc.Container:

    """
    This function constructs the main dashboard layout for 

    Args:
        df: pd.DataFrame
            DataFrame containing golf course data with columns validated
            via data pipeline.

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

    initial_fig = map_golf_courses(df)

    rounds = df['number_of_rounds'].sum()

    top_courses = get_top_bottom_courses(df, top=True)
    bottom_courses = get_top_bottom_courses(df, top=False)

    return dbc.Container([
            # Header Section
            create_page_header(
                    header_title="Akin's Golf Dashboard",
                    subtitle=(f"Performance analysis by golf course of {rounds} "
                             "rounds played since 2016"),
                    footer_text="Data tracked and visualized using Python, Dash, and Plotly",
                    icon_class="globe-europe-africa"),

            # Stat Cards
            #'Stat cards',

            # Map golf courses
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            # Title
                            html.H5("Akin's Course Analytics", className="card-title"),

                            # Select Course Type
                            html.Div(
                                [
                                dbc.Label("Pick course type:",
                                          # "mb-0" removes the bottom margin labels usually have
                                          # "me-2" adds a small gap between label and the buttons
                                          className="fw-bold text-primary mb-1 me-2"),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "All courses", "value": "all"},
                                        {"label": "18 hole courses only", "value": "18 hole"},
                                        {"label": "9 hole courses only", "value": "9 hole"},
                                    ],
                                    value="all",
                                    id="radioitems-inline-input",
                                    inline=True,
                                    # "d-flex" here helps if the buttons themselves are misaligned
                                    className="d-flex align-items-center"
                                ),
                                ],
                                # "d-flex" makes the label and radio group sit in a row
                                # "align-items-center" vertically centers items
                                className="d-flex align-items-center mb-2"
                            ),

                            # 2. Top 5 Courses Row
                            create_course_badges(
                                header_title="Top 5 scoring venues (avg vs par)",
                                badge_id="top_course_badges",
                                courses=top_courses,
                                header_colour="success"),

                            # --- Bottom 5 ROW ---
                            create_course_badges(
                                header_title="Bottom 5 scoring venues (avg vs par)",
                                badge_id="bottom_course_badges",
                                courses=bottom_courses,
                                header_colour="warning"),

                            # The Map
                            dcc.Graph(
                                id="golf_map",
                                figure=initial_fig,
                                config={"displayModeBar": False},
                                style={"height": "500px", "marginTop": "-2.5px"},
                                )
                                    ],)
                            ], className="shadow-sm mb-2")
                        ], width=12)
                    ])

        ], fluid=True) # Close Container

# Callbacks for home page tab
@callback(
    [Output("golf_map", "figure"),
    Output("top_course_badges_course_1", "children"),
    Output("top_course_badges_course_2", "children"),
    Output("top_course_badges_course_3", "children"),
    Output("top_course_badges_course_4", "children"),
    Output("top_course_badges_course_5", "children"),
    Output("bottom_course_badges_course_1", "children"),
    Output("bottom_course_badges_course_2", "children"),
    Output("bottom_course_badges_course_3", "children"),
    Output("bottom_course_badges_course_4", "children"),
    Output("bottom_course_badges_course_5", "children")],
    [Input("radioitems-inline-input", "value"),
     Input("main-data", "data")]
)
def update_course_types(course_type, main_data):

    """
    Filters golf course data by type and generates updated map and ranking components.

    This function deserializes a JSON string into a DataFrame, filters the courses 
    based on the provided 'course_type' category, and then invokes helper functions 
    to produce a geographic visualization and statistical rankings.

    Args:
        course_type (str): The category of golf course to filter by. 
            Expected values: "all", "18 hole", "9 hole", or "9 hole - par 3 course".
        main_data (str): A JSON-formatted string containing the golf course records 
            (must be compatible with pd.read_json(orient='records')).

    Returns:
        tuple: A triplet containing:
            - golf_map (obj): The output from map_golf_courses (typically a Figure or HTML).
            - top_courses (pd.DataFrame): The highest-rated courses based on the filter.
            - bottom_courses (pd.DataFrame): The lowest-rated courses based on the filter.
        """

     # Convert stored JSON data back to DataFrame
    df = pd.read_json(StringIO(main_data), orient='records')

    # Filter the DataFrame based on the selected course type
    match course_type:

        case "all":
            filtered_df = df

        case "18 hole":
            filtered_df = df[df['course_type'] == "18 hole"]

        case "9 hole":
            filtered_df = df[df['course_type'].isin(["9 hole", "9 hole - par 3 course"])]

    golf_map = map_golf_courses(filtered_df)
    top_courses = get_top_bottom_courses(filtered_df, top=True)
    bottom_courses = get_top_bottom_courses(filtered_df, top=False)

    return (golf_map,
            f"1. {top_courses[0]}", f"2. {top_courses[1]}", f"3. {top_courses[2]}",
            f"4. {top_courses[3]}", f"5. {top_courses[4]}",
            f"1. {bottom_courses[0]}", f"2. {bottom_courses[1]}", f"3. {bottom_courses[2]}",
            f"4. {bottom_courses[3]}", f"5.   {bottom_courses[4]}")
