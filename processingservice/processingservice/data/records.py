from datetime import datetime

from pydantic import BaseModel


class BaseDataRecord(BaseModel):
    latitude: float
    longitude: float
    datetime_utc: datetime


class WeatherRecord(BaseDataRecord):
    temp: float
    precip: float
    pressure: float
    humidity: float
    wind_speed: float


class OpenAQRecord(BaseDataRecord):
    parameter: str
    value: float


class InputRecord(BaseModel):
    datetime_utc: datetime
    device_id: str | None

    parameter: str
    value: float | None

    weather: WeatherRecord

    latitude: float
    longitude: float
    country: str | None

    sensors_type: int | None
    chip_id: str | None
    location_id: int | None
    street_name: str | None
    city: str | None
    deployment_date: datetime | None


class PredictedRecord(BaseModel):
    datetime_utc: datetime
    device_id: str

    parameter: str
    value: float
