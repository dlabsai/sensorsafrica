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


class InputRecord(BaseModel):
    datetime_utc: datetime
    device_id: str

    parameter: str
    value: float | None

    weather: WeatherRecord

    latitude: float
    longitude: float
    sensors_type: str
    country: str

    chip_id: str
    location_id: int
    street_name: str
    city: str
    country: str
    deployment_date: datetime


class PredictedRecord(BaseModel):
    datetime_utc: datetime
    device_id: str

    parameter: str
    value: float