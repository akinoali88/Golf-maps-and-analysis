"""
Base graph functions for 
"""

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
import plotly.graph_objects as go

def map_golf_courses(df: pd.DataFrame) -> Figure:

    """
    Generates an interactive geographic visualization of golf course locations.

    This function maps individual courses using coordinate data, with visual 
    encoding for both frequency of play (marker size) and scoring performance 
    (marker color). It is specifically styled for a clean, professional dashboard 
    look.

    Args:
        df (pd.DataFrame): The dataset containing course metadata and aggregate 
            statistics. Required columns: 'latitude', 'longitude', 'course', 
            'number_of_rounds', 'avg_over_par', 'par', 'avg_score', 'best_score', 
            'course_index', and 'slope_rating'.

    Returns:
        plotly.graph_objects.Figure: A localized map (centered on SE England) 
            featuring:
            - Bubble markers scaled to the total number of rounds played.
            - Diverging color scale (Red-Yellow-Green) based on average score vs. par.
            - A 'Carto Voyager' basemap with minimal labeling for clarity.
            - Custom legend-style annotation explaining circle size logic.
            - Comprehensive hover tooltips including Slope Rating and Course Index.

    Notes:
        The layout uses 'scattermode="group"' to mitigate marker overlap in 
        geographically dense areas. The color axis is intentionally reversed 
        ('RdYlGn_r') so that lower scores (better performance) appear green.
    """

    fig = px.scatter_map(
        df,
        lat="latitude",
        lon="longitude",
        text="course",
        size="number_of_rounds",
        size_max=35,
        color="avg_over_par",
        color_continuous_scale="RdYlGn_r",
        center={
            "lat": 51.26,
            "lon": 0.65},
        zoom=8.5,
        hover_name="course",
        hover_data={
            "number_of_rounds": True,
            "par": True,
            "avg_score": True,
            "avg_over_par": True,
            "best_score": True,
            "course_index": True,
            "slope_rating": True,
            "latitude": False,
            "longitude": False,
            },
        labels={
            "number_of_rounds": "Rounds Played",
            "avg_over_par": "Average Score Over Par",
            "avg_score": "Average Score",
            "course_index": "Course Index",
            "slope_rating": "Slope Rating",        
            }
        )

    # Update trace to position text
    fig.update_traces(
        textposition="bottom right",
        mode="markers+text",
        textfont=dict(
            size=12,
                ),
    )

    # Update color axis to adjust colorbar title and position
    fig.update_coloraxes(
        colorbar=dict(
            title=dict(text="<b>Average Score<br>Over Par</b>",
            ),
            x=1.02,
            ticks="outside"
        )
    )

    # Add annotation to explain circle size
    fig.add_annotation(
        text="○ Circle size denotes number of rounds",
        xref="paper", yref="paper",
        x=0.02, y=0.05,        # Positions it in the bottom left
        showarrow=False,
        font=dict(size=12, color="black"),
        bgcolor="lightgrey",
        bordercolor="gray",
        borderwidth=1,
        borderpad=4,
        opacity=0.8
    )

    # Update hovertemplate for datapoints
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{hovertext}</b>",
            "Rounds Played: %{customdata[0]}",
            "Par: %{customdata[1]}",
            "Avg Score: %{customdata[2]:.1f}",
            "Avg Over Par: %{customdata[3]:.1f}",
            "Best Score: %{customdata[4]}",
            "Course Index: %{customdata[5]}",
            "Slope Rating: %{customdata[6]}",
        ])
    )

    # Update map style and prevent points from overlapping
    fig.update_layout(
        map_style="carto-voyager-nolabels",
        scattermode="group")    # Prevent points from overlapping

    # Add light box around map area
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color="lightgrey",
                    width=2,
                ),
            )
        ],
        #margin=dict(l=10, r=10, t=10, b=10) # Optional: adds a tiny bit of breathing room
)

    return fig

def plot_score_over_time(df: pd.DataFrame,
                         rolling_window: int = 10,
                         ) -> Figure:

    """
    Generates a multi-layered time-series visualization of golf performance.

    The chart plots individual round scores (normalized to 18-hole 'effective' 
    scores) and overlays statistical trends to highlight improvement or 
    regression over time.

    Args:
        df (pd.DataFrame): The dataset containing golf rounds. Required columns 
            include 'date', 'effective scove over par', 'course', 'holes_played', 
            'score', 'over_par', 'eff_score_label', 'rolling_best', and 'rolling_worst'.
        rolling_window (int, optional): The number of rounds to include in the 
            moving average and best/worst calculations. Defaults to 10.
        min_periods (int, optional): Minimum number of observations in window 
            required to have a value. Defaults to 2.

    Returns:
        plotly.graph_objects.Figure: A comprehensive performance chart featuring:
            - Scatter points colored by score (Red-Yellow-Green scale).
            - A rolling average trendline for overall performance direction.
            - "Best" and "Worst" boundary lines (dotted) with a light-shaded 
              performance corridor.
            - Custom hover tooltips with per-round details and course names.

    Notes:
        The Y-axis and color bar are formatted to always display signs (e.g., +4, -2) 
        to maintain golf-centric reporting. The legend is positioned horizontally 
        above the chart for better mobile responsiveness.
    """

    fig = px.scatter(df,
                     x="date",
                     y="effective score over par",
                     title=("Golf Performance Trends<br>"
                     "<sup>Relative to Par (Normalized to 18 Holes)</sup>"),
                     symbol="course_type",
                     color="effective score over par",
                     color_continuous_scale="RdYlGn_r",
                     labels={
                         "date": "Date of Round",
                         "effective score over par": "Effective Score Over Par",
                         "course_type": "Course Type"},
                     hover_name="course",
                     hover_data={
                         "date": True,
                         "holes_played": True,
                         "score": True,
                         "over_par": True,
                         "eff_score_label": True,
                     },
                                          )

    chart_width = 0.8  # Chart takes up 80% of the width, leaving 20% for legend and margins

    # Move legend above the chart and make it horizontal
    fig.update_layout(
        legend=dict(
            title_text="",    # Remove default legend title since we titles by legendgroup
            orientation="v",      # Vertical orientation
            x=chart_width+0.02,           # Starts just after the chart ends
            y=1,              # Align to top
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(0,0,0,0)",    # Transparent background to prevent overlap issues

            # Adjust this number (in pixels) for more/less space between legend groups
            tracegroupgap=40,
        ),
        xaxis=dict(
            domain=[0, chart_width],    # Chart only takes up 70% of the width
            range=[df['date'].min(), df['date'].max()]
        ),
        yaxis=dict(
            # '+d' = Always show sign, integer format
            # '+.1f' = Always show sign, 1 decimal place (best for 'effective' scores)
            tickformat="+d",
        ),

        coloraxis_colorbar=dict(
            title="<b>Effective Score<br>Over Par</b>",
            tickformat="+d",  # Always show the + or - sign
            len=0.8,           # Shortens it slightly so it doesn't crowd the margins
            y=1.02,
            yanchor="top",
        ),
        # Optional: Add top margin so the legend doesn't get cut off
        margin=dict(t=80)
    )

    # Update hovertemplate for scatter points
    fig.update_traces(
        legendgroup="courses",
        legendgrouptitle_text="<b>Course Types</b>",
        selector=dict(mode="markers"),
        hovertemplate="<br>".join([
            "<b>%{hovertext}</b>",
            "Date: %{x}",
            "Holes played: %{customdata[0]}",
            "Score: %{customdata[1]}",
            "Over Par: %{customdata[2]:+d}",
            "%{customdata[3]}",    # Effective score label only visible for non-18 hole rounds
            ]),
        marker=dict(
            line=dict(
                width=1,
                color='DarkSlateGrey' # Or 'white' if you want them to pop more
                ),
            ),
    )

    # Update trendline name to reflect rolling window size
    # We use a loop to find the trendline safely in case the order changes
    for trace in fig.data:
        if "trend" in trace.name.lower() or "rolling" in trace.name.lower():
            trace.name = f"{rolling_window}-Round Rolling Average Score"

    # Add Rolling Best Line (Lower is better in golf, so usually Green)
    fig.add_scatter(
        x=df['date'],
        y=df['rolling_best'],
        mode='lines',
        name=f'{rolling_window}-Round Rolling Best Score',
        line=dict(color='rgba(40, 167, 69, 0.4)', width=2, dash='dot'), # Translucent green
        legendgroup='Rolling scores',
        hovertemplate=f"Rolling {rolling_window}-Round Best: %{{y:+d}}<extra></extra>"
    )

    # Add Rolling Worst Line (Higher is worse, so usually Red)
    fig.add_scatter(
        x=df['date'],
        y=df['rolling_worst'],
        mode='lines',
        fill='tonexty',
        legendgroup='Rolling scores',
        legendgrouptitle_text="<b>Rolling Average Ranges</b>",
        name=f'{rolling_window}-Round Rolling Worst Score',
        fillcolor='rgba(220, 53, 69, 0.05)', # Very light green fill
        line=dict(color='rgba(220, 53, 69, 0.4)', width=2, dash='dot'), # Translucent red
        hovertemplate=f"Rolling {rolling_window}-Round Worst: %{{y:+d}}<extra></extra>"
    )

    # Add Rolling Average line (Dashed Blue)
    fig.add_scatter(
        x=df['date'],
        y=df['rolling_average'],
        mode='lines',
        legendgroup='Rolling scores',
        name=f'{rolling_window}-Round Rolling Average Score',
        fillcolor='rgba(220, 53, 69, 0.05)', # Very light green fill
        line=dict(color='rgba(220, 53, 69, 0.4)', width=2, dash='dot'), # Translucent red
        hovertemplate=f"Rolling {rolling_window}-Round Average: %{{y:+d}}<extra></extra>"
    )

    # Add light box around axes
    fig.update_xaxes(showline=True, linewidth=.5, linecolor="lightgrey", mirror=True)
    fig.update_yaxes(showline=True,
                     linewidth=.5,
                     linecolor="lightgrey",
                     mirror=True,
                     gridwidth=0.25,
                     gridcolor='lightgrey',
                     griddash='dot')

    return fig

def performance_radar_chart(
        avg_metrics: pd.Series,           # pre-computed overall average (never changes)
        course_metrics: pd.Series = None,  # filtered course trace (from callback)
        course: str = None
                            ) -> Figure:
    """
    Generates a radar chart comparing average performance across key golf metrics.

    Produces a radar (spider) chart with up to two traces: a baseline trace
    showing overall average performance across all courses, and an optional
    second trace showing the selected course's average performance for direct
    comparison.

    Args:
        avg_metrics (pd.Series): Pre-computed overall average performance values
            indexed by metric name. Used as the baseline trace and must contain
            values for all five metrics: Driving, Irons, Approach Play, Chipping,
            and Putting.
        course_metrics (pd.Series, optional): Average performance values for the
            selected course, indexed by metric name. When provided, renders as a
            second trace for comparison against the overall average. Defaults to None.
        course (str, optional): Name of the selected course, used as the legend
            label for the course trace. Only relevant when course_metrics is
            provided. Defaults to None.

    Returns:
        Figure: A Plotly Figure object containing a polar scatter chart with:
            - A blue 'Overall Average' trace (always present).
            - A red course-specific trace (present only when course_metrics
            is provided).
            - A vertical legend positioned to the right of the chart.
            - A radial axis scaled from 0 to 10.s

    """

    rank_cols = ["Overall Performance", "Driving", "Irons", "Approach Play", "Chipping", "Putting"]

    def make_traces(series):
        r = list(series.reindex(rank_cols)) + [series.reindex(rank_cols).iloc[0]]
        theta = rank_cols + [rank_cols[0]]
        return r, theta

    fig = go.Figure()

    # Trace 1: overall average (always present)
    r_avg, theta = make_traces(avg_metrics)

    fig.add_trace(go.Scatterpolar(
        r=r_avg, theta=theta,
        fill='toself', name='Overall Average',
        line=dict(color='royalblue', width=2),
        fillcolor='rgba(65, 105, 225, 0.2)',
    ))

    # Trace 2: selected course (added when filter is applied)
    if course_metrics is not None:
        r_course, theta = make_traces(course_metrics)
        fig.add_trace(go.Scatterpolar(
            r=r_course, theta=theta,
            fill='toself', name=course,
            line=dict(color='tomato', width=2),
            fillcolor='rgba(255, 99, 71, 0.2)',
        ))

    fig.update_layout(
        title=dict(
            text='Performance Breakdown',
            x=0.35,
            xanchor='left',
            font=dict(size=14),
        ),
        polar=dict(radialaxis=dict(visible=True, range=[0, 10], tickvals=[2, 4, 6, 8, 10])),
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.1,
        ),
        margin=dict(t=40, b=60, l=60, r=60),
        height=420,
    )

    return fig
