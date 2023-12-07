import pandas as pd

from processingservice.data.records import InputRecord


def get_dataset(records: list[InputRecord]) -> pd.DataFrame:
    return pd.DataFrame.from_records([pd.json_normalize(r.model_dump(), sep='__') for r in records])
