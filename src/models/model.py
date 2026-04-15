''' 
Create pydantic model 
'''


from enum import Enum
import re
from typing import ClassVar, Union, Literal, Annotated
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_extra_types.coordinate import Longitude, Latitude
from pydantic_extra_types.country import CountryAlpha3



class GolfCourseTypes(str, Enum):

    """Golf course types"""

    NINE_HOLE_PAR_3 = '9 hole - par 3 course'
    NINE_HOLE = '9 hole'
    EIGHTEEN_HOLE = '18 hole'

class GameFormat(str, Enum):

    """Golf game formats"""

    STROKE_PLAY = 'Stroke Play'
    SCRAMBLE = 'Scramble'
    WILD_GOLF = 'Wild Golf'

def snake_to_space_title(field_name: str) -> str:

    """
    Converts a snake_case string to a Title Case string with spaces.

    This is primarily used as an alias generator for Pydantic models to map 
    Pythonic attribute names to human-readable data headers (e.g., CSV columns).

    Args:
        field_name (str): The snake_case string to convert (e.g., 'golf_course').

    Returns:
        str: The converted string (e.g., 'Golf Course').

    Example:
        >>> snake_to_space_title("country_code")
        'Country Code'
        
    Note:
        This function uses .title(), which may capitalize internal acronyms 
        incorrectly (e.g., 'iso_code' becomes 'Iso Code' instead of 'ISO Code').
    """

    # Converts 'country_code' to 'Country Code'
    return field_name.replace("_", " ").title()

# UK Postcode Regex (simplified but robust version)
UK_POSTCODE_REGEX = r"^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$"

# France Postcode Regex (exactly 5 digits)
FR_POSTCODE_REGEX = r"^\d{5}$"

class GolfCourse(BaseModel):

    '''Class representing feeding data for a child'''

    model_config = ConfigDict(
        alias_generator=snake_to_space_title,
        populate_by_name=True
    )

    course_name: str
    country: str
    country_code: CountryAlpha3
    course_type: GolfCourseTypes
    address: str = Field(min_length=5, max_length=150)
    post_code: str
    latitude: Latitude
    longitude: Longitude
    par: int
    course_index: float
    slope_rating: int = Field(ge=55, le=155)

    # Check that for par 3 courses, par is 27
    @model_validator(mode='after')
    def validator_par_for_course_type(self):

        """
        Validates that par for par 3 courses is 27
        """

        if self.course_type == GolfCourseTypes.NINE_HOLE_PAR_3 and self.par != 27:
            raise ValueError(
                f"For a 9 Hole Par 3 course, par must be 27. Received: {self.par}")

        if self.course_type == GolfCourseTypes.NINE_HOLE and not 28 <= self.par <= 37:
            raise ValueError(
                f"For a 9 Hole course, par must be between 28 and 37. Received: {self.par}")

        if self.course_type == GolfCourseTypes.EIGHTEEN_HOLE and not 68 <= self.par <= 74:
            raise ValueError(
                f"For an 18 Hole course, par must be between 68 and 74. Received: {self.par}")

        return self

    # Check that post code format is consistent with country standard
    @model_validator(mode='after')
    def check_postcode_by_country(self):

        """
        Validates the postcode format is consistent with country stadard
        It currently supports GBR (UK) and FRA (France).
        """

        if self.country_code == 'GBR':
            if not re.match(UK_POSTCODE_REGEX, self.post_code):
                raise ValueError(f"Invalid UK postcode format: {self.post_code}")

        elif self.country_code == 'FRA':
            if not re.match(FR_POSTCODE_REGEX, self.post_code):
                raise ValueError(f"France postcodes must be exactly 5 digits: {self.post_code}")

        return self

    @model_validator(mode='after')
    def validate_par_against_course_type(self) -> 'GolfCourse':

        """
        Checks that par for courses is consistent with course type
        """

        course_type = self.course_type
        par = self.par

        if course_type == GolfCourseTypes.NINE_HOLE_PAR_3:
            if par != 27:
                raise ValueError(f"For a 9 Hole Par 3 course, par must be 27. Received: {par}")

        elif course_type == GolfCourseTypes.NINE_HOLE:
            if not 28 <= par <= 45:
                raise ValueError(f"For a 9 Hole course, par must be between 28 and 45."
                                 f"Received: {par}")

        elif course_type == GolfCourseTypes.EIGHTEEN_HOLE:
            if not 68 <= par <= 74:
                raise ValueError("For an 18 Hole course, par must be "
                                 f"between 68 and 74. Received: {par}")

        return self

    # set label for class for reporting
    label: ClassVar[str] = 'golf courses'

class GolfRounds(BaseModel):

    """
    Class to capture key round date. 
    Extras are allowed to capture performance indicators and these
    will be validated with an additional basemodel for performance
    """

    model_config = ConfigDict(
        extra='ignore',
        alias_generator=snake_to_space_title,
        populate_by_name=True
    )

    round_number: int = Field(ge=1)
    course: str
    date: date
    year: int = Field(ge=2016, le=datetime.now().year)
    format: GameFormat
    holes_played: int = Field(alias="Holes")
    score: int
    effective_score: int
    over_par: int

    # set label for class for reporting
    label: ClassVar[str] = 'golf rounds'

# Setup for RoundPerformance Indicators
# Define reusable types

# 1. A basic rank (0-10)
# We use float to allow for half-points (e.g., 7.5)
RankScore = Annotated[float, Field(ge=0, le=10)]
Count = Annotated[float, Field(ge=0)]

OptionalCount = Union[Count, Literal["not recorded"]]

class RoundPerformance(BaseModel):

    """
    Add performance indicators to golf round data

    This is kept separate from the base GolfRounds model to allow for flexibiliy where users
    may not have performance data
    """

    model_config = ConfigDict(
        alias_generator=snake_to_space_title,
        populate_by_name=True)

    round_number: int = Field(ge=1)

    # optional as driving not required for all courses (e.g., par 3 courses)
    driving: Union[
        RankScore,
        Literal["not recorded"]] = Field(default="not recorded")

    # Required fields for all rounds
    duff_drives: Count
    irons: RankScore
    inside_100_yards: RankScore
    chipping: RankScore
    shots_lost_in_bunkers: Count
    putting: RankScore

    # Optional stats not available for all rounds
    duff_shots: OptionalCount = "not recorded"
    triple_bogeys: OptionalCount = "not recorded"
    scores_of_8_plus: OptionalCount = Field(default="not recorded", alias="Scores of 8+")

    # set label for class for reporting
    label: ClassVar[str] = 'golf round performance'
