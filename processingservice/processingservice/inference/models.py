import pandas as pd

from processingservice.inference.base import BasePredictor
from processingservice.awsadapters.loaders import load_model_from_s3


class PM1Predictor(BasePredictor):
    def __init__(self) -> None:
        self.model = load_model_from_s3("sensorsafrica", "models/model_pm1.pkl")

    def predict(self, data: pd.DataFrame):
        data["pred"] = self.model.predict(data)
        return data["pred"]
