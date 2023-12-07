import pandas as pd
from datetime import timezone

from processingservice.data.parameters import AirQualityParameter
from processingservice.data.records import InputRecord


def process_dataset(df: pd.DataFrame) -> pd.DataFrame:
    result_df = pd.DataFrame()
    result_df["timestamp"] = pd.to_datetime(
        df["timestamp"], format="%Y-%m-%d %H:%M:%S.%f %z"
    ).dt.tz_convert("UTC")
    result_df["device_id"] = df["device_id"]
    result_df["parameter"] = df["parameter"]
    result_df = result_df[
        result_df["parameter"].isin([p.value for p in AirQualityParameter])
    ]
    result_df["value"] = df["value"]
    result_df["location_id"] = df["location_id"]
    result_df["hour"] = df["timestamp"].dt.hour
    result_df["month"] = df["timestamp"].dt.month.astype(str)
    result_df["month_day"] = (
        df["timestamp"].dt.month.astype(str) + "_" + df["timestamp"].dt.day.astype(str)
    )
    result_df["year_month_day"] = (
        df["timestamp"].dt.year.astype(str)
        + "_"
        + df["timestamp"].dt.month.astype(str)
        + "_"
        + df["timestamp"].dt.day.astype(str)
    )

    result_df = result_df.groupby(
        [
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

    return result_df


def get_datasets(
    records: list[InputRecord],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.DataFrame.from_records(
        [pd.json_normalize(r.model_dump(), sep="__") for r in records]
    )
    df = process_dataset(df)
    df_pm_1 = df[df["parameter"] == AirQualityParameter.PM_1.value]
    df_pm_2_5 = df[df["parameter"] == AirQualityParameter.PM_2_5.value]
    df_pm_10 = df[df["parameter"] == AirQualityParameter.PM_10.value]

    return df_pm_1, df_pm_2_5, df_pm_10
