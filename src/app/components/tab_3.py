'''
Render the 3rd page
'''

# from io import StringIO
# from dash import dcc, html, callback, Input, Output
# from dash.exceptions import PreventUpdate

from io import StringIO

from dash import html, callback,  dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from src.app.dashboard_logic import create_page_header, create_stat_card
from src.app.base_graphs import performance_radar_chart


def render_page3(df: pd.DataFrame,
                 performance_df: pd.DataFrame) -> dbc.Container:

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

    items = df['course'].sort_values().unique().tolist()

    # this needs work....
    initial_fig = performance_radar_chart(performance_df)

    return dbc.Container([

            # Header Section
            create_page_header(
                    header_title='Course Detail',
                    subtitle='Breakdown of scores and performance details at specific courses',
                    footer_text='Based on rounds completed since 2016',
                    icon_class='card-list'),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5('Course Performance Breakdown',
                                    className='card-title'),

                            # Select course
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        dcc.Dropdown(
                                            options=items,
                                            value=items[0],
                                            id='demo-dropdown',
                                            style={'color': '#777'}),
                                    ])
                                ], width=4), # 4 out of 12 columns = 1/3 of the page
                            ]),

                            # Key summary
                            dbc.Row([
                                create_stat_card('Rounds Played',
                                                 'rounds-played',
                                                 'primary'),

                                create_stat_card('Average Score',
                                                 'avg-score',
                                                 'primary'),

                                create_stat_card('Average Score (vs Par)',
                                                 'avg-score-vs-par',
                                                 'primary'),

                                create_stat_card('Best Score',
                                                 'best-score',
                                                 'success'),

                                create_stat_card('Worst Score',
                                                 'worst-score',
                                                 'warning'),

                                create_stat_card('Course Ranking',
                                                 'course-ranking',
                                                 'primary'),

                                    ], className='mt-3 mb-3'),

                            # performance radar plot
                            dcc.Graph(id='avg-feed-volume',
                                        figure=initial_fig,
                                        config={'displayModeBar': False},
                                        style={'height': '350px'},
                                        )
                        ])
                    ], className='shadow mb-4')
                ], lg=12, md=12)
            ]) # Close Row
            ], fluid=True) # Close Container


@callback(
    [Output('rounds-played', 'children'),
    Output('avg-score', 'children'),
    Output('avg-score-vs-par', 'children'),
    Output('best-score', 'children'),
    Output('worst-score', 'children'),
    Output('course-ranking', 'children'),],
    [Input('demo-dropdown', 'value'),
     Input('course-data', 'data')]
)
def update_output(value, course_data):

    """
    Filters golf round data by course and calculates performance statistics.

    This function takes a JSON string of course data, converts it to a DataFrame, 
    and displays key metrics for a specific course, including total rounds 
    played, scoring averages, and score extremes.

    Args:
        value (str): The name of the course to filter the data by.
        course_data (str): A JSON-formatted string containing the course summary records 
            (must be compatible with pandas 'records' orientation).

    Returns:
        tuple: A tuple of six formatted strings:
            - rounds_played (str): Total number of rounds played at the course.
            - avg_score (str): Mean score formatted to two decimal places.
            - avg_score_vs_par (str): Mean score relative to par (two decimal places).
            - best_score (str): The highest numerical score recorded.
            - worst_score (str): The lowest numerical score recorded.
            - course_ranking (str): Rank of course versus of same course type
                (18 hole, 9 hole, etc.) based on average score vs par.

    """

    # Convert stored JSON data back to DataFrame
    df = pd.read_json(StringIO(course_data), orient='records')

    filtered_df = df.loc[df['course'] == value]

    # Ensure scalar values using .iloc[0]
    rounds_played = filtered_df['number_of_rounds'].iloc[0]
    avg_score = filtered_df['avg_score'].iloc[0]
    avg_score_vs_par = filtered_df['avg_over_par'].iloc[0]
    best_score = filtered_df['best_score'].iloc[0]
    worst_score = filtered_df['worst_score'].iloc[0]
    course_ranking = filtered_df['rank_label'].iloc[0]

    return (f'{rounds_played}',
            f'{avg_score:.0f}',
            f'{avg_score_vs_par:+.1f}',
            f'{best_score}', f'{worst_score}', f'{course_ranking}')
