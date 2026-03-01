

'''
Module for dashboard logic functions including
create state card and create page header

'''
from typing import List

import dash_bootstrap_components as dbc
from dash import html

def create_stat_card(title: str,
                     id_name: str,
                     text_color: str ='primary',
                     width: int =4) -> dbc.Col:
    '''
    Returns a Bootstrap Column containing a styled Card for metrics.

    Parameters:
        title : str
            The title text to display at the top of the card.
        id_name : str
            The HTML id attribute for the card's H2 element, used for dynamic content updates.
        text_color : str, optional
            The text color class suffix for Bootstrap styling (default is 'primary').
            Examples: 'primary', 'success', 'danger', 'warning', 'info'
        width : int, optional
            The Bootstrap grid width (1-12) for the column (default is 4).
    Returns:
        dbc.Col
            A Dash Bootstrap Column component containing a Card with centered,
            styled metric display. The card includes a muted title header and
            a large H2 element for the metric value.

    '''
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H6(title,
                        className='text-muted mb-0',
                        style={'fontSize': '0.9rem'}),
                html.H2(id=id_name,
                        className=f'text-{text_color} mb-0')
            ], className='py-2')
        ], className='text-center shadow-sm'),
        width=width
    )


def create_page_header(header_title: str,
                       subtitle: str,
                       footer_text: str ='',
                       icon_class: str = None) -> dbc.Card:
    '''
    Creates a standardized, reusable header card for dashboard pages.
    This function generates a header card that includes a main title, a subtitle, 
    and an optional footer text. The card is designed to maintain a consistent 
    appearance across different dashboard pages, enhancing the user interface 
    and user experience.
    
    Parameters:
        header_title : str
            The main title to be displayed prominently at the top of the card.
        subtitle : str
            A brief description or subtitle that provides additional context 
            related to the header title.
        footer_text : str, optional
            An optional text displayed at the bottom of the card. This can be used 
            for additional information or notes. Defaults to an empty string.
        icon_class : str, optional
            The Bootstrap Icon class (e.g., 'bi-droplet-fill').
            If provided, it appears above the footer_text.

            Find icon libary here: https://icons.getbootstrap.com/
    Returns:
        dbc.Card
            A Dash Bootstrap Component Card object containing the formatted header 
            with the specified title, subtitle, and footer text.
        
    '''

    # Prepare the icon element if a class is provided
    # This version handles it whether you pass "droplet" or "bi-droplet"
    icon_element = None

    if icon_class:
        icon_to_display = icon_class.replace('bi-', '')
        icon_element = html.I(
            className=f"bi bi-{icon_to_display} text-primary mb-1",
            style={'fontSize': '2rem'}
    )
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H2(header_title,
                                className='text-primary fw-bold mb-0'),
                        html.P(subtitle,
                                className='text-muted small mb-0 italic'),
                    ], className='ps-3 border-start border-primary border-4')
                ], width=8),

                # Right side: Icon (top) and Footer Text (bottom)
                dbc.Col(
                    html.Div([
                        icon_element,
                        html.Small(footer_text, className='text-muted'),
                    ], className='d-flex flex-column align-items-end'),
                    width=4, className='align-self-center'
                )
            ], className='align-items-center')
        ], className='py-2 px-3')
    ],
    className='shadow-sm border-0 mb-3 mt-3',
    style={'borderRadius': '10px'}
    )


def create_course_badges(
        header_title: str,
        courses: List[str],
        header_colour: str = 'success') -> dbc.Row:

    """
    Creates a styled Dash Bootstrap Row featuring a color-coded title label 
    followed by a series of course badges.

    This helper is designed to sit above charts or maps to call out specific 
    segments like 'Top 5' or 'Bottom 5' courses. It uses a horizontal 'pill' 
    layout where the title has a solid background and courses are listed 
    as light-colored badges.

    Args:
        header_title (str): The text to display in the leading colored box 
            (e.g., 'Top 5').
        courses (List[str]): A list of course names or identifiers to be 
            rendered as badges.
        header_colour (str): The Bootstrap theme color for the title column 
            background. Defaults to 'success'. Common values include 
            'success', 'danger', 'primary', or 'warning'.

    Returns:
        dbc.Row: A formatted Dash Bootstrap Row component ready for 
            insertion into a layout.
    """

    # Validation: Ensure courses list is not empty to avoid rendering issues
    if len(courses) == 0 or courses is None:
        raise ValueError('The courses list cannot be empty. '
                         'Please provide at least one course name.')


    title_class = f'bg-{header_colour} text-white rounded-start p-2 text-start'

    badge_class = (
        'bg-light d-flex align-items-center rounded-end'
        'border-top border-bottom border-end'
    )


    return  dbc.Row([
    # Label Column with Success background
    dbc.Col(
        html.Span(header_title, className='fw-bold'),
        style={"width": "320px", "flex": "0 0 320px", "maxWidth": "100%"},
        className=title_class
    ),
    # Courses Column with Secondary/Light badges
    dbc.Col([
        dbc.Badge(
                # This f-string combines the number and the name
                f"{i}. {course}",
                color='light',
                text_color='dark',
                className='ms-2 border shadow-sm'
            ) for i, course in enumerate(courses, 1) # '1' tells it to start counting at 1
        ], className=badge_class)
                ], className='mx-0 mb-2')

def get_top_bottom_courses(df,count=5, top=True):
    """
    Extracts and formats a list of courses based on their performance.

    This helper sorts the DataFrame by 'avg_over_par' and retrieves either 
    the top (lowest scores) or bottom (highest scores) courses, returning 
    them as a list of strings formatted for UI display.

    Args:
        df (pd.DataFrame): The DataFrame containing golf course data. 
            Must include 'course' and 'avg_over_par' columns.
        count (int): The number of courses to retrieve. Defaults to 5.
        top (bool): If True, retrieves courses with the lowest avg_over_par. 
            If False, retrieves those with the highest. Defaults to True.

    Returns:
        List[str]: A list of strings in the format "Course Name (Score)".
    """

    # Determine if we want the top or bottom of the sorted list
    subset = (df.sort_values('avg_over_par').head(count) if top
                else df.sort_values('avg_over_par').tail(count))

    # Return the formatted list of strings
    return [
        f"{course} ({score:.1f})"
        for course, score in subset[['course', 'avg_over_par']].itertuples(index=False, name=None)
    ]
