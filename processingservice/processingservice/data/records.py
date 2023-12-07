from datetime import datetime

from pydantic import BaseModel


class BaseDataRecord(BaseModel):
    latitude: float
    longitude: float
    datetime_utc: datetime


class WeatherRecord(BaseDataRecord):
    temp: float
    precip: float
    snow: float
    pressure: float
    humidity: float
    wind_speed: float
    wind_gust: float | None


class OpenAQRecord(BaseDataRecord):
    parameter: str
    value: float


class InputRecord(WeatherRecord, OpenAQRecord):
    parameter: str
    value: float

    sensors_type: str
    country: str

    chip_id: str
    device_id: str
    location_id: int
    street_name: str
    city: str
    country: str
    deployment_date: datetime
