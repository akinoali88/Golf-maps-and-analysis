'''
Tests file for data aggregation functions. 
'''

# Import your function from your specific file
from src.pipeline.data_transformation import generate_course_summaries


def test_aggregation_math(sample_golf_data):
    """Verify that the min, max, and mean calculations are accurate."""
    rounds, courses = sample_golf_data
    result = generate_course_summaries(rounds, courses)

    # Filter for St Andrews to check stats
    st_andrews = result[result['course'] == 'St Andrews'].iloc[0]

    assert st_andrews['number_of_rounds'] == 3
    assert st_andrews['best_score'] == 70
    assert st_andrews['avg_score'] == 75.0
    assert st_andrews['worst_score'] == 80

def test_merge_completeness(sample_golf_data):
    """Verify that the course metadata merges correctly."""
    rounds, courses = sample_golf_data
    result = generate_course_summaries(rounds, courses)

    # Check that metadata columns exist and aren't empty
    assert 'slope_rating' in result.columns
    assert result.loc[result['course'] == 'Augusta', 'slope_rating'].values[0] == 140

def test_column_selection(sample_golf_data):
    """Verify that only the requested columns are returned from the courses DF."""
    rounds, courses = sample_golf_data

    # Add an extra column that shouldn't be in the final output
    courses['secret_notes'] = 'Don\'t include me'

    result = generate_course_summaries(rounds, courses)
    assert 'secret_notes' not in result.columns
