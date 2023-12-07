import pandas as pd
from ..awsadapters.loaders import load_csv_from_s3
from .dummy import DummyPM25Predictor, DummyPM10Predictor
from .models import PM1Predictor


def load_predictors():
    return PM1Predictor(), DummyPM25Predictor(), DummyPM10Predictor()


def load_user_uploaded_data_from_storage(location: str) -> pd.DataFrame:
    return load_csv_from_s3(location)
