from .base import BaseModel, ValidationError
from .user import User
from .weather_station import UserStation, WeatherStation


MODELS = [User, WeatherStation, UserStation]
