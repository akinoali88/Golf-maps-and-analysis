''' Test file for data processing functions '''

from src.pipeline.data_processing import process_golf_courses, process_golf_rounds


# --- TESTS FOR: process_golf_courses ---

def test_process_golf_courses_removes_nulls(course_data):
    """Ensure None, NaN, and empty strings are stripped out."""
    df_cleaned = process_golf_courses(course_data)

    # Should remove: Augusta(1), 2 nulls, 2 empties = 5 rows removed
    # Should keep: Augusta(1), Pebble Beach(1), St Andrews(1) = 3 rows total
    assert len(df_cleaned) == 3
    assert not df_cleaned['Course Name'].isna().any()
    assert '   ' not in df_cleaned['Course Name'].values

def test_process_golf_courses_deduplication(course_data):
    """Ensure duplicate course names are reduced to one entry."""
    df_cleaned = process_golf_courses(course_data)

    # Augusta appears twice in the fixture; should only appear once now
    augusta_count = len(df_cleaned[df_cleaned['Course Name'] == 'Augusta'])
    assert augusta_count == 1

def test_process_golf_courses_copy_integrity(course_data):
    """Ensure the function returns a new object (doesn't mutate the original)."""
    df_cleaned = process_golf_courses(course_data)
    assert df_cleaned is not course_data


# --- TESTS FOR: process_golf_rounds ---

def test_process_golf_rounds_returns_original(round_data):
    """The function currently returns the original DF; verify this behavior."""
    df_result = process_golf_rounds(round_data)
    assert len(df_result) == len(round_data)
    assert list(df_result.columns) == list(round_data.columns)

def test_process_golf_rounds_logic(capsys, round_data):
    """
    Test the print outputs (since the function only prints warnings 
    rather than dropping rows).
    """
    process_golf_rounds(round_data)
    captured = capsys.readouterr()

    assert "Found 2 duplicate rows" in captured.out
    assert "Found 1 duplicate round ids" in captured.out
