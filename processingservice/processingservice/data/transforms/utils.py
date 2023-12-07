from collections import defaultdict
from datetime import timedelta, datetime, date

from processingservice.data.parameters import AirQualityParameter
from ..records import InputRecord


def generate_date_hours(start_date: datetime, end_date: datetime) -> set[tuple[date, int]]:  # noqa: E501
    date_hours = set()
    current_date = start_date
    while current_date <= end_date:
        for hour in range(24):
            date_hours.add((current_date.date(), hour))
        current_date += timedelta(days=1)
    return date_hours


def find_missing_date_hours_for_pm_readings(records: list[InputRecord]) -> dict[tuple[str, str], list[tuple[date, int]]]:  # noqa: E501]):
    if not records:
        return {}

    # Find the range of dates
    start_date = min(record.datetime_utc for record in records)
    end_date = max(record.datetime_utc for record in records)

    all_date_hours = generate_date_hours(start_date, end_date)
    records_by_parameter_sensor = defaultdict(set)

    key: tuple[str, str]
    for record in records:
        date_hour = (record.datetime_utc.date(), record.datetime_utc.hour)
        if record.parameter not in [p.value for p in AirQualityParameter]:
            continue
        key = (record.parameter, record.device_id)
        records_by_parameter_sensor[key].add(date_hour)

    missing_date_hours = {}
    for (parameter, sensors_type), date_hours in records_by_parameter_sensor.items():
        missing_hours = sorted(all_date_hours - date_hours)
        if missing_hours:
            missing_date_hours[(parameter, sensors_type)] = missing_hours

    return missing_date_hours
