"""
Aggregation functions to prepare data for reporting and analysis.
"""

import pandas as pd

def generate_course_summaries(golf_rounds: pd.DataFrame,
                              golf_courses: pd.DataFrame, ) -> pd.DataFrame:

    """
    Aggregrate scoring data from golf rounds at golf course level
    
    Args:
        golf_rounds (pd.DataFrame): DataFrame containing golf rounds data, 
            validated with the GolfRounds pydantic basemodel class
        golf_courses (pd.DataFrame): DataFrame containing golf course data, 
            validated with the GolfCourse pydantic basemodel class

        
    Returns:
        pd.DataFrame: Aggregated DataFrame.
    """

    # Step Aggregate golf round data at course level

    course_round_summary = golf_rounds.groupby("course").agg(
        course=("course", "first"),
        number_of_rounds=("course", "count"),
        best_score=("score", "min"),
        avg_score=("score", "mean"),
        worst_score=("score", "max"),
        best_over_par=("over_par", "min"),
        avg_over_par=("over_par", "mean"),
        worst_over_par=("over_par", "max"),
        ).reset_index(drop=True)

    # Select critical golf course information only.
    golf_course_data = golf_courses.loc[:,
        ["course_name",
        "course_type",
        "par",
        "country_code",
        "latitude",
        "longitude",
        "course_index",
        "slope_rating",
        ]].copy()

    # Merge with golf course data to round data
    course_round_summary = course_round_summary.merge(
        golf_course_data,
        left_on="course",
        right_on="course_name").drop(columns=["course_name"])

    return course_round_summary

def transform_round_summaries(golf_rounds: pd.DataFrame,
                              golf_course: pd.DataFrame,
                              rolling_window: int = 10,
                              min_periods: int = 2
                              ) -> pd.DataFrame:

    """
    Transforms the golf rounds data to prepare for time series analysis and visualisation.
    
    Args:
        golf_rounds (pd.DataFrame): DataFrame containing golf rounds data, 
            validated with the GolfRounds pydantic basemodel class

        golf_courses (pd.DataFrame): DataFrame containing golf course data, 
            validated with the GolfCourse pydantic basemodel class
    Returns:
        pd.DataFrame: Transformed DataFrame with additional time-based features.
    """

    # Get course type
    golf_rounds = golf_rounds.merge(
        golf_course[["course_name", "course_type"]],
        left_on="course",
        right_on="course_name",
        how="left").drop(columns=["course_name"])

    # Get effective score over par per round,
    # normalised to 18 holes to allow for comparison across rounds of different lengths
    golf_rounds["effective scove over par"] = (
        golf_rounds["over_par"] / golf_rounds["holes_played"] * 18)

    # Create the conditional label for Effective Score
    # only applicable for rounds with less than 18 holes played
    golf_rounds['eff_score_label'] = golf_rounds.apply(
        lambda x: f"Effective Over Par: {x['effective scove over par']:+.1f}"
        if x['holes_played'] != 18 else "",
        axis=1
        )

    # Sort by date to ensure the rolling window makes sense chronologically
    golf_rounds = golf_rounds.sort_values("date")

    # Calculate rolling metrics
    golf_rounds['rolling_best'] = (golf_rounds['effective scove over par'].
                                   rolling(window=rolling_window, min_periods=min_periods).min())
    golf_rounds['rolling_worst'] = (golf_rounds['effective scove over par'].
                                    rolling(window=rolling_window, min_periods=min_periods).max())
    golf_rounds['rolling_average'] = (golf_rounds['effective scove over par'].
                                    rolling(window=rolling_window, min_periods=min_periods).mean())

    return golf_rounds
