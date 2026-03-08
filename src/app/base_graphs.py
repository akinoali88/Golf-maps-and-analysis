"""
Base graph functions for 
"""

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

def map_golf_courses(df: pd.DataFrame) -> Figure:

    """
    Docstring for map_golf_courses
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: Figure
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

    fig.update_layout()

    # Update trace to position text
    fig.update_traces(
        textposition="bottom right",
        mode="markers+text",
        textfont=dict(
            size=12,
                ),
    )

    fig.update_coloraxes(
        colorbar=dict(
            title=dict(text="<b>Average Score<br>Over Par</b>",
            ),
            x=1.02,
            ticks="outside"
        )
    )

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

    fig.update_layout(
        map_style="carto-voyager-nolabels",
        scattermode="group")    # Prevent points from overlapping

    return fig

def plot_score_over_time(df: pd.DataFrame,
                         rolling_window: int = 10,
                         ) -> Figure:

    """
    Docstring for plot_score_over_time
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: Figure
    """

    fig = px.scatter(df,
                     x="date",
                     y="effective scove over par",
                     title=("Golf Performance Trends<br>"
                     "<sup>Relative to Par (Normalized to 18 Holes)</sup>"),
                     symbol="course_type",
                     color="effective scove over par",
                     trendline="rolling",
                     trendline_options=dict(window=rolling_window),
                     trendline_scope="overall",
                     color_continuous_scale="RdYlGn_r",
                     labels={
                         "date": "Date of Round",
                         "effective scove over par": "Effective Score Over Par",
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

    # Move legend above the chart and make it horizontal
    fig.update_layout(
        legend=dict(
            orientation="h",      # Horizontal orientation
            yanchor="bottom",     # Anchors the legend's bottom to the 'y' coordinate
            y=1.02,               # Places it just above the top of the chart (y=1)
            xanchor="right",      # Anchors the right side of the legend
            x=1                   # Aligns the right side of legend with right side of chart
        ),
        xaxis=dict(
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
            len=0.8           # Shortens it slightly so it doesn't crowd the margins
        ),
        # Optional: Add top margin so the legend doesn't get cut off
        margin=dict(t=80)
    )

    fig.update_traces(
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

    trendline_hovertemplate = (
        f"<b>Rolling {rolling_window} round average score</b><br>" +
        "Rolling average score: +%{y:.1f}<br>")

    # Update trendline hovertemplate for rolling average
    fig.update_traces(
        selector=dict(mode="lines"),
        hovertemplate=trendline_hovertemplate)

    # Add Rolling Best Line (Lower is better in golf, so usually Green)
    fig.add_scatter(
        x=df['date'],
        y=df['rolling_best'],
        mode='lines',
        name=f'{rolling_window}-Round Best',
        line=dict(color='rgba(40, 167, 69, 0.4)', width=2, dash='dot'), # Translucent green
        hovertemplate=f"Rolling {rolling_window}-Round Best: %{{y:+d}}<extra></extra>"
    )

    # Add Rolling Worst Line (Higher is worse, so usually Red)
    fig.add_scatter(
        x=df['date'],
        y=df['rolling_worst'],
        mode='lines',
        fill='tonexty',
        name=f'{rolling_window}-Round Worst',
        fillcolor='rgba(220, 53, 69, 0.05)', # Very light green fill
        line=dict(color='rgba(220, 53, 69, 0.4)', width=2, dash='dot'), # Translucent red
        hovertemplate=f"Rolling {rolling_window}-Round Worst: %{{y:+d}}<extra></extra>"
    )

    # Add light box around axes
    fig.update_xaxes(showline=True, linewidth=.5, linecolor="lightgrey", mirror=True)
    fig.update_yaxes(showline=True, linewidth=.5, linecolor="lightgrey", mirror=True)

    return fig
