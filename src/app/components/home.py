"""
Render the home tab for ....
"""

from io import StringIO

# from dash.exceptions import PreventUpdate
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output
from src.app.dashboard_logic import create_page_header, create_course_badges, get_top_bottom_courses
from src.app.base_graphs import map_golf_courses

def render_home_tab(df: pd.DataFrame) -> dbc.Container:

    """
    Constructs the primary dashboard layout for the 'Home' tab.

        This function aggregates high-level stats and assembles the layout components, 
        including the page header, filtering controls, performance leaderboards, 
        and the geographic map of golf courses.

        Args:
            df (pd.DataFrame): The processed golf dataset. Must contain 'number_of_rounds' 
                and columns required by 'map_golf_courses' and 'get_top_bottom_courses'.

        Returns:
            dbc.Container: A fluid Bootstrap container containing:
                - A dynamic header displaying total rounds played.
                - Radio buttons for filtering data by course type (18-hole vs 9-hole).
                - Top 5 and Bottom 5 performance badges (avg vs. par).
                - An interactive Plotly map centered on course locations.

        Notes:
            The layout relies on Dash Bootstrap Components (DBC) for responsiveness. 
            Interactive elements are linked to the `update_course_types` callback via 
            component IDs.

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
                                    id="radioitems-course-type",
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
                                ),
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
    [Input("radioitems-course-type", "value"),
     Input("course-data", "data")]
)
def update_course_types(course_type, main_data):

    """
    Filters the golf dataset and updates the map and leaderboard badges.

    Triggered when the user changes the course type radio buttons or when the 
    underlying client-side data store is updated. It performs data filtering 
    and re-calculates the top/bottom 5 venues.

    Args:
        course_type (str): The filter category selected ("all", "18 hole", or "9 hole").
        main_data (str): JSON-serialized DataFrame from the dcc.Store component.

    Returns:
        tuple: A collection of 11 elements matching the callback Outputs:
            - [0]: plotly.graph_objects.Figure: The updated geographic map.
            - [1-5]: str: Formatted strings for the Top 5 course badges.
            - [6-10]: str: Formatted strings for the Bottom 5 course badges.

    Raises:
        ValueError: If main_data cannot be parsed or required columns are missing.
        """

     # Convert stored JSON data back to DataFrame
    df = pd.read_json(StringIO(main_data), orient='records')

    # Filter the DataFrame based on the selected course type
    match course_type:

        case "all":
            filtered_df = df

        case "18 hole":
            filtered_df = df[df["course_type"] == "18 hole"]

        case "9 hole":
            filtered_df = df[df["course_type"].isin(["9 hole", "9 hole - par 3 course"])]

    golf_map = map_golf_courses(filtered_df)
    top_courses = get_top_bottom_courses(filtered_df, top=True)
    bottom_courses = get_top_bottom_courses(filtered_df, top=False)

    return (golf_map,
            f"1. {top_courses[0]}", f"2. {top_courses[1]}", f"3. {top_courses[2]}",
            f"4. {top_courses[3]}", f"5. {top_courses[4]}",
            f"1. {bottom_courses[0]}", f"2. {bottom_courses[1]}", f"3. {bottom_courses[2]}",
            f"4. {bottom_courses[3]}", f"5.   {bottom_courses[4]}")
