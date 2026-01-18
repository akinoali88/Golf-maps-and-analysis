''' 
Create pydantic model 
'''


from enum import Enum
import re
from pydantic import BaseModel, ConfigDict, model_validator
from pydantic_extra_types.coordinate import Longitude, Latitude


class GolfCourseTypes(str, Enum):

    '''Golf course types'''

    NINE_HOLE_PAR_3 = '9 hole - par 3 course'
    NINE_HOLE = '9 hole'
    EIGHTEEN_HOLE = '18 hole'

def snake_to_space_title(field_name: str) -> str:

    '''
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
    '''

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
    country_code: str
    course_type: GolfCourseTypes
    address: str
    post_code: str
    latitude: Latitude
    longitude: Longitude
    par: int
    course_index: float
    slope_rating: int


    @model_validator(mode='after')
    def check_postcode_by_country(self):

        if self.country_code == 'GBR':
            if not re.match(UK_POSTCODE_REGEX, self.post_code):
                raise ValueError(f"Invalid UK postcode format: {self.post_code}")

        elif self.country_code == 'FRA':
            if not re.match(FR_POSTCODE_REGEX, self.post_code):
                raise ValueError(f"France postcodes must be exactly 5 digits: {self.post_code}")

        return self
