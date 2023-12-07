from datetime import date
from functools import lru_cache
from ..clients.weather.api import get_weather
from ..records import WeatherRecord


@lru_cache(maxsize=32)
def get_weather_record(
    latitude: float, longitude: float, day: date, hour: int
) -> WeatherRecord:
    weather_records = get_weather(
        coordinates=f"{latitude}, {longitude}",
        date_from=day.strftime("%Y-%m-%d"),
        date_to=day.strftime("%Y-%m-%d"),
    )

    for record in weather_records:
        if record.datetime_utc.day == day.day and record.datetime_utc.hour == hour:
            return record

    raise ValueError(f"Record not found for {latitude}, {longitude} - {day} {hour}")
