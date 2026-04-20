'''
Render the 3rd page
'''

# from io import StringIO
# from dash import dcc, html, callback, Input, Output
# from dash.exceptions import PreventUpdate

from io import StringIO

from dash import html, callback,  dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from src.app.dashboard_logic import create_page_header, create_stat_card
from src.app.base_graphs import performance_radar_chart


def render_page3(df: pd.DataFrame,
                 avg_performance_metrics: pd.DataFrame
                 ) -> dbc.Container:

    """
        Constructs the layout for the Course Detail page (Page 3) of the golf
    analytics dashboard.

    This function builds a Dash Bootstrap Container comprising a page header,
    a course selector dropdown, summary statistic cards, and a performance
    radar chart. Statistic cards and the radar chart are updated dynamically
    via the update_output callback when the dropdown selection changes.

    Parameters:
        df (pd.DataFrame): Course-level summary data. Must contain a 'course'
            column used to populate the dropdown options.
        avg_performance_metrics (pd.Series): Pre-computed overall average
            performance values indexed by metric name (e.g. Driving, Irons,
            Putting). Used to render the baseline trace of the radar chart
            on initial load.

    Returns:
        dbc.Container: A fluid Bootstrap container containing:
            - A page header with title, subtitle, and footer text.
            - A course selector dropdown (id: demo-dropdown).
            - Six summary stat cards showing rounds played, average score,
            average score vs par, best score, worst score, and course ranking.
            - A radar chart (id: performance-radar) comparing performance
            metrics for the selected course against the overall average.

    Notes:
        The component uses Dash Bootstrap Components for responsive layout and
        styling. Chart interactions and statistics updates are handled via the
        update_output callback using the component IDs defined in this function.
        The stores course-data, performance-store, and avg-performance-store
        must be present in the parent layout for the callback to function.


    """


    items = df['course'].sort_values().unique().tolist()

    # this needs work....
    initial_fig = performance_radar_chart(avg_performance_metrics)

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
                            html.Div(
                                [
                                    html.H5('Select Course:',
                                            className='fw-bold text-primary mb-0 me-2',
                                            style={'whiteSpace': 'nowrap'}),
                                    html.Div(
                                        dcc.Dropdown(
                                            options=items,
                                            value=items[0],
                                            id='demo-dropdown',
                                            style={'color': '#777'}
                                        ),
                                        style={'width': '20%'}
                                    ),
                                ],
                                style={'display': 'flex', 'alignItems': 'center'}
                            ),

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
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id='performance-radar',
                                        figure=initial_fig,
                                        config={'displayModeBar': False},
                                        )],
                                        width=6),
                                dbc.Col([ html.Div("Your other content here") ], width=6),
                            ])

                        ])
                    ], className='shadow mb-2')
                ], lg=12, md=12)
            ]) # Close Row
            ], fluid=True) # Close Container


@callback(
    Output('rounds-played', 'children'),
    Output('avg-score', 'children'),
    Output('avg-score-vs-par', 'children'),
    Output('best-score', 'children'),
    Output('worst-score', 'children'),
    Output('course-ranking', 'children'),
    Output('performance-radar', 'figure'),
    Input('demo-dropdown', 'value'),
    State('course-data', 'data'),
    State('performance-store', 'data'),
    State('avg-performance-store', 'data'),
    State('round-data', 'data'),
)

def update_output(course_name, course_data, performance_data, avg_performance_data, round_data):

    """
    Dash callback that filters golf data by selected course and returns updated
    statistics and a performance radar chart.

    Args:
        course_name (str): The name of the selected course from the dropdown.
        course_data (str): JSON string (records orientation) containing course-level
            summary statistics, including rounds played, scoring averages, and rankings.
        performance_data (str): JSON string (records orientation) containing per-round
            performance metrics (e.g. Driving, Irons, Putting) with columns
            'course', 'performance_metric', and 'performance_value'.
        avg_performance_data (dict): Serialised dict mapping performance metric names
            to their overall average values, used to render the baseline radar trace.

    Returns:
        tuple: A 7-element tuple of Dash component values:
            - rounds_played (str): Total rounds played at the selected course.
            - avg_score (str): Mean score rounded to the nearest integer.
            - avg_score_vs_par (str): Mean score vs par, formatted with sign (e.g. '+4.2').
            - best_score (str): Lowest score recorded at the course.
            - worst_score (str): Highest score recorded at the course.
            - course_ranking (str): Course rank within its category (e.g. 18-hole)
                based on average score vs par.
            - output_fig (Figure): Radar chart comparing overall average performance
                against the selected course's average across key metrics.

    Returns no_update if any required input is missing or None.

    """

    # Convert stored JSON data back to DataFrame
    if not course_name or not course_data or not performance_data or not avg_performance_data:
        return no_update

    df = pd.read_json(StringIO(course_data), orient='records')
    performance_df = pd.read_json(StringIO(performance_data), orient='records')
    round_df = pd.read_json(StringIO(round_data), orient='records')
    avg_performance_metrics = pd.Series(avg_performance_data)

    filtered_df = df.loc[df['course'] == course_name]
    round_df = round_df.loc[round_df['course'] == course_name]

    # Ensure scalar values using .iloc[0]
    rounds_played = filtered_df['number_of_rounds'].iloc[0]
    avg_score = filtered_df['avg_score'].iloc[0]
    avg_score_vs_par = filtered_df['avg_over_par'].iloc[0]
    best_score = filtered_df['best_score'].iloc[0]
    worst_score = filtered_df['worst_score'].iloc[0]
    course_ranking = filtered_df['rank_label'].iloc[0]

    # Get performance metrics for the selected course
    rank_cols = ["Overall Performance", "Driving", "Irons", "Approach Play", "Chipping", "Putting"]

    course_metrics = (
        performance_df[
            (performance_df['course'] == course_name) &
            (performance_df['performance_metric'].isin(rank_cols))
        ]
        .groupby('performance_metric')['performance_value']
        .mean()
    )

    output_fig = performance_radar_chart(avg_performance_metrics, course_metrics, course_name)

    # Prepare data for table of recent rounds
    table_cols = [ 'date', 'year', 'format', 'holes_played',
       'score', 'over_par',]

    #need to sort by date to show last 5 rounds
    print(round_df.sort_values('date', ascending=False)[table_cols].head())

    return (f'{rounds_played}',
            f'{avg_score:.0f}',
            f'{avg_score_vs_par:+.1f}',
            f'{best_score}', f'{worst_score}', f'{course_ranking}',
            output_fig)
