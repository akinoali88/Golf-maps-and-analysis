''' 
Create pydantic model 
'''

from datetime import datetime

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Data(BaseModel):

    '''Class representing feeding data for a child'''

    var_1: int
    var_2: float
    date_var: datetime

class ChildConfig(BaseModel):

    '''Schema for private data'''
    item_1: str
    item_2: str

class AppSettings(BaseSettings):

    '''Main settings class that reads from .env'''


    # Tell Pydantic to look for a .env file
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

# Create a singleton instance to use throughout your app
settings = AppSettings()
