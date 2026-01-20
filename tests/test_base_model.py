'''
< insert docstring here>
'''

import unittest

import pytest
from pydantic import ValidationError
from src.models.model import GolfCourse


# --- Tests ---

def test_valid_golf_course_instantiation(valid_golf_course_data):
    """Test that valid data creates a model successfully."""
    course = GolfCourse(**valid_golf_course_data)
    assert course.course_name == "St Andrews Links"
    assert course.slope_rating == 132

def test_alias_population(valid_golf_course_data):
    """Test that aliases (Space Title) work alongside snake_case names."""
    # Test via the alias (from the fixture)
    course = GolfCourse(**valid_golf_course_data)
    assert course.course_name == "St Andrews Links"

    # Test via the snake_case name (populate_by_name=True)
    valid_golf_course_data['course_name'] = "Pebble Beach"
    del valid_golf_course_data['Course Name']
    course = GolfCourse(**valid_golf_course_data)
    assert course.course_name == "Pebble Beach"

def test_invalid_slope_rating(valid_golf_course_data):
    """Test the constraints (ge=55, le=155) on slope_rating."""
    valid_golf_course_data["Slope Rating"] = 50  # Below 55
    with pytest.raises(ValidationError) as excinfo:
        GolfCourse(**valid_golf_course_data)
    assert "Input should be greater than or equal to 55" in str(excinfo.value)

    valid_golf_course_data["Slope Rating"] = 160  # Above 155
    with pytest.raises(ValidationError):
        GolfCourse(**valid_golf_course_data)

def test_address_length_constraints(valid_golf_course_data):
    """Test the min/max length constraints on address."""
    # Too short
    valid_golf_course_data["Address"] = "A"
    with pytest.raises(ValidationError):
        GolfCourse(**valid_golf_course_data)

    # Too long
    valid_golf_course_data["Address"] = "A" * 151
    with pytest.raises(ValidationError):
        GolfCourse(**valid_golf_course_data)

@pytest.mark.parametrize("invalid_code", ["GB", "UNITED KINGDOM", "123"])
def test_invalid_country_code(valid_golf_course_data, invalid_code):
    """Test that CountryAlpha3 only accepts 3-letter codes."""
    valid_golf_course_data["Country Code"] = invalid_code
    with pytest.raises(ValidationError):
        GolfCourse(**valid_golf_course_data)


if __name__ == '__main__':
    unittest.main()
