import pandas as pd
from datetime import datetime

from processingservice.data.parameters import AirQualityParameter
from processingservice.data.records import InputRecord


def get_datasets(
    records: list[InputRecord],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.DataFrame.from_records(
        [pd.json_normalize(r.model_dump(), sep="__") for r in records]
    )
    df_pm_1 = df[df["parameter"] == AirQualityParameter.PM_1.value]
    df_pm_2_5 = df[df["parameter"] == AirQualityParameter.PM_2_5.value]
    df_pm_10 = df[df["parameter"] == AirQualityParameter.PM_10.value]

    return df_pm_1, df_pm_2_5, df_pm_10


def string_to_datetime(date_string: str) -> datetime:
    # Define the format matching the input string
    date_format = "%Y-%m-%d %H:%M:%S.%f %z"

    # Convert the string to a datetime object
    return datetime.strptime(date_string, date_format)


def build_input_records(csv_file) -> list[InputRecord]:
    df = pd.read_csv(csv_file)
    records = []
    for _, row in df.iterrows():
        try:
            value = float(row["value"])
        except ValueError:
            value = None

        try:
            sensors_type = int(row["sensors_type"])
        except ValueError:
            sensors_type = None

        latitude = float(row["latitude"])
        longitude = float(row["longitude"])

        records.append(
            InputRecord(
                datetime_utc=string_to_datetime(row["timestamp"]),
                device_id=row["device_id"],

                parameter=row["parameter"],
                value=value,

                weather=get_weather_record(latitude, longitude),

                latitude=latitude,
                longitude=longitude,
                country=row["country"],

                sensors_type=sensors_type,
                chip_id=row["chip_id"],
                location_id=row["location_id"],
                street_name=row["street_name"],
                city=row["city"],

                deployment_date=string_to_datetime(row["deployment_date"]),
            )
        )
    return records
