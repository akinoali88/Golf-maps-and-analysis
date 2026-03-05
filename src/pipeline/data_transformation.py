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

def transform_round_summaries(golf_rounds: pd.DataFrame) -> pd.DataFrame:

    """
    Transforms the golf rounds data to prepare for time series analysis and visualisation.
    
    Args:
        golf_rounds (pd.DataFrame): DataFrame containing golf rounds data, 
            validated with the GolfRounds pydantic basemodel class
    Returns:
        pd.DataFrame: Transformed DataFrame with additional time-based features.
    """

    # Get effective score over par per round,
    # normalised to 18 holes to allow for comparison across rounds of different lengths
    golf_rounds["effective scove over par"] = (
        golf_rounds["over_par"] / golf_rounds["holes_played"] * 18)

    return golf_rounds
