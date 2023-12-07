from datetime import date
from functools import lru_cache
from ..clients.weather.api import get_weather
from ..records import WeatherRecord


@lru_cache(maxsize=32)
def get_weather_record(latitude: float, longitude: float, day: date) -> WeatherRecord:
    weather_records = get_weather(
        coordinates=f"({latitude}, {longitude})",
        date_from=day.strftime("%Y-%m-%d"),
        date_to=day.strftime("%Y-%m-%d")
    )
