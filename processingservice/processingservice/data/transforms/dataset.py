import pandas as pd
from datetime import datetime, timezone

from processingservice.data.parameters import AirQualityParameter
from processingservice.data.records import InputRecord

from .getters import get_weather_record


def get_datasets(
    records: list[InputRecord],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.json_normalize([r.model_dump() for r in records], sep="__")
    df_pm_1 = df[df["parameter"] == AirQualityParameter.PM_1.value]
    df_pm_2_5 = df[df["parameter"] == AirQualityParameter.PM_2_5.value]
    df_pm_10 = df[df["parameter"] == AirQualityParameter.PM_10.value]

    return df_pm_1, df_pm_2_5, df_pm_10


def string_to_datetime(date_string: str) -> datetime:
    # Define the format matching the input string
    date_format = "%Y-%m-%d %H:%M:%S.%f %z"

    # Convert the string to a datetime object
    return datetime.strptime(date_string, date_format)


def build_input_records_for_inference(csv_file: str | None = None, csv_as_df: pd.DataFrame | None = None) -> list[InputRecord]:
    if csv_file is None and csv_as_df is None:
        raise ValueError("Either csv_file or csv_as_df must be provided")

    if csv_file is not None:
        csv_as_df = pd.read_csv(csv_file)

    records = []
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

                weather=get_weather_record(latitude, longitude, datetime_utc.date(), datetime_utc.hour),

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
    return records
