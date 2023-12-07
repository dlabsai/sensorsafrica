from datetime import datetime
from logging import getLogger

import openaq

from processingservice.data.records import OpenAQRecord

logger = getLogger(__name__)

api = openaq.OpenAQ()

DEFAULT_PARAMETERS = ["pm25", "pm10"]


def get_measurements(
    coordinates: str, date_from: str, date_to: str
) -> list[OpenAQRecord]:
    """
    Provides air quality data

    :param coordinates: coordinates (lat, long)
    :param date_from: date from in format Y-M-D
    :param date_to: date to in format Y-M-D
    :return: list of records
    """
    logger.info(f"Getting data for {coordinates} - from {date_from} to {date_to}")

    status, result = api.measurements(
        coordinates=coordinates,
        parameters=DEFAULT_PARAMETERS,
        date_from=date_from,
        date_to=date_to,
    )
    measurements = []

    if status != 200:
        raise ConnectionError("API connection error")

    for measurement in result["results"]:
        measurements.append(
            OpenAQRecord(
                latitude=measurement["coordinates"]["latitude"],
                longitude=measurement["coordinates"]["longitude"],
                datetime_utc=datetime.fromisoformat(measurement["date"]["utc"]),
                parameter=measurement["parameter"],
                value=measurement["value"],
            )
        )

    return measurements
