import pandas as pd

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
