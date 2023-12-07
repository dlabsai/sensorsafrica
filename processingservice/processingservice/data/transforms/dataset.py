import pandas as pd
from datetime import datetime, timezone, timedelta

from processingservice.data.parameters import AirQualityParameter
from processingservice.data.records import InputRecord

from .getters import get_weather_record
from .utils import find_missing_date_hours_for_pm_readings


def process_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        df["parameter"].isin([p.value for p in AirQualityParameter])
    ]

    result_df = pd.DataFrame()
    result_df["timestamp"] = df["datetime_utc"].astype(str).str.slice(0, 19)
    result_df["timestamp"] = pd.to_datetime(
        result_df["timestamp"], format="%Y-%m-%d %H:%M:%S"
    )
    result_df["device_id"] = df["device_id"]
    result_df["parameter"] = df["parameter"]

    result_df["weather__temp"] = df["weather__temp"]
    result_df["weather__precip"] = df["weather__precip"]
    result_df["weather__pressure"] = df["weather__pressure"]
    result_df["weather__humidity"] = df["weather__humidity"]
    result_df["weather__wind_speed"] = df["weather__wind_speed"]

    result_df["value"] = df["value"]
    result_df["location_id"] = df["location_id"]
    result_df["hour"] = result_df["timestamp"].dt.hour
    result_df["month"] = result_df["timestamp"].dt.month.astype(str)
    result_df["month_day"] = (
        result_df["timestamp"].dt.month.astype(str) + "_" + result_df["timestamp"].dt.day.astype(str)
    )
    result_df["year_month_day"] = (
        result_df["timestamp"].dt.year.astype(str)
        + "_"
        + result_df["timestamp"].dt.month.astype(str)
        + "_"
        + result_df["timestamp"].dt.day.astype(str)
    )

    result_df["year_month_day_hour"] = (
        result_df["timestamp"].dt.year.astype(str)
        + "_"
        + result_df["timestamp"].dt.month.astype(str)
        + "_"
        + result_df["timestamp"].dt.day.astype(str)
        + "_"
        + result_df["timestamp"].dt.hour.astype(str)
    )

    result_df = result_df.groupby(
        [
            "year_month_day_hour",
            "device_id",
            "parameter",
            "year_month_day",
            "hour",
            "month",
            "month_day",
            "location_id",
            "weather__temp",
            "weather__precip",
            "weather__pressure",
            "weather__humidity",
            "weather__wind_speed",
        ],
        as_index=False,
    )["value"].mean()
    result_df["avg_value_year_month_day"] = result_df.groupby(
        ["location_id", "parameter", "year_month_day"], as_index=False
    )["value"].transform("mean")
    """
    result_df["avg_value_year_month_day_hour_location"] = result_df.groupby(
        ["hour", "month", "month_day", "location_id", "parameter", "year_month_day"],
        as_index=False,
    )["value"].transform("mean")
    """

    result_df = result_df.drop('device_id', axis=1)
    result_df = result_df.drop('location_id', axis=1)
    return result_df


def get_datasets(
    records: list[InputRecord],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.json_normalize([r.model_dump() for r in records], sep="__")

    df = process_dataset(df)

    df_pm_1 = df[df["parameter"] == AirQualityParameter.PM_1.value]
    df_pm_2_5 = df[df["parameter"] == AirQualityParameter.PM_2_5.value]
    df_pm_10 = df[df["parameter"] == AirQualityParameter.PM_10.value]

    return df_pm_1, df_pm_2_5, df_pm_10


def string_to_datetime(date_string: str) -> datetime:
    # Define the format matching the input string
    date_format = "%Y-%m-%d %H:%M:%S.%f %z"

    # Convert the string to a datetime object
    return datetime.strptime(date_string, date_format)


def build_input_records_for_inference(
    csv_file: str | None = None, csv_as_df: pd.DataFrame | None = None
) -> list[InputRecord]:
    if csv_file is None and csv_as_df is None:
        raise ValueError("Either csv_file or csv_as_df must be provided")

    if csv_file is not None:
        csv_as_df = pd.read_csv(csv_file)

    records = []

    # Firstly, build InputRecord objects for each row in the CSV file
    for _, row in csv_as_df.iterrows():
        try:
            value = float(row["value"])
        except ValueError:
            value = None

        try:
            sensors_type = int(row["sensor_type"])
        except ValueError:
            sensors_type = None

        latitude = float(row["latitude"])
        longitude = float(row["longitude"])

        # Convert timestamp to datetime in UTC
        datetime_utc = string_to_datetime(row["timestamp"]).astimezone(timezone.utc)

        records.append(
            InputRecord(
                datetime_utc=datetime_utc,
                device_id=str(row["device_id"]),
                parameter=str(row["parameter"]),
                value=value,
                weather=get_weather_record(
                    latitude, longitude, datetime_utc.date(), datetime_utc.hour
                ),
                latitude=latitude,
                longitude=longitude,
                country=str(row["country"]),
                sensors_type=sensors_type,
                chip_id=str(row["chip_id"]),
                location_id=row["location_id"],
                street_name=str(row["street_name"]),
                city=str(row["city"]),
                deployment_date=string_to_datetime(row["deployment_date"]),
            )
        )

    # Secondly, fill in missing records with None as a missing parameter for each sensor.
    # We look only for missing PM values.
    missing_date_hours = find_missing_date_hours_for_pm_readings(records)

    for sensor, date_hours in missing_date_hours.items():
        for date_hour in date_hours:
            row = csv_as_df[csv_as_df['device_id'] == int(sensor[1])].iloc[0].to_dict()

            latitude = float(row["latitude"])
            longitude = float(row["longitude"])

            records.append(
                InputRecord(
                    datetime_utc=datetime(date_hour[0].year, date_hour[0].month, date_hour[0].day, date_hour[1]),
                    device_id=sensor[1],
                    parameter=sensor[0],
                    value=None,
                    weather=get_weather_record(
                        latitude, longitude, date_hour[0], date_hour[1]
                    ),
                    latitude=latitude,
                    longitude=longitude,
                    country=str(row["country"]),
                    sensors_type=None,
                    chip_id=str(row["chip_id"]),
                    location_id=row["location_id"],
                    street_name=str(row["street_name"]),
                    city=str(row["city"]),
                    deployment_date=string_to_datetime(row["deployment_date"]),
                )
            )

    return records
