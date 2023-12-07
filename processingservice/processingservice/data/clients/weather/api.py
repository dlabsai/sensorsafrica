import os
from datetime import datetime
from logging import getLogger

import requests

from processingservice.data.records import WeatherRecord

logger = getLogger(__name__)


API_URL = os.getenv("WEATHER_API_URL")
API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(
    coordinates: str, date_from: str, date_to: str, include: str = "hours"
) -> list[WeatherRecord]:
    """
    Get weather records
    :param coordinates: coordinates (lat, long)
    :param date_from: date from in format Y-M-D
    :param date_to: date to in format Y-M-D
    :param include: sections included in the result data
    :return: List of weather records
    """
    url = f"{API_URL}/services/timeline/{coordinates}/{date_from}/{date_to}?unitGroup=metric&key={API_KEY}&include={include}"

    logger.info(f"Getting data for {coordinates} - from {date_from} to {date_to}")
    response = requests.get(url)

    if response.status_code != 200:
        raise ConnectionError("API connection error")

    data = response.json()
    weather_records = []

    for day in data["days"]:
        for hour in day["hours"]:
            timestamp_string = f"{day['datetime']} {hour['datetime']}"
            timestamp = datetime.strptime(timestamp_string, "%Y-%m-%d %H:%M:%S")
            pressure = hour.get("pressure")
            if pressure is None:
                pressure = 1000.0
            weather_records.append(
                WeatherRecord(
                    latitude=data["latitude"],
                    longitude=data["longitude"],
                    datetime_utc=timestamp,
                    temp=hour["temp"],
                    precip=hour["precip"],
                    pressure=pressure,
                    humidity=hour["humidity"],
                    wind_speed=hour["windspeed"],
                )
            )

    return weather_records
