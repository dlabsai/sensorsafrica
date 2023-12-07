import pandas as pd

from processingservice.inference.base import BasePredictor


class BaseDummyPredictor(BasePredictor):
    def predict(self, data: pd.DataFrame):
        data["pred"] = 0
        return data["pred"]


class DummyPM1Predictor(BaseDummyPredictor):
    pass


class DummyPM25Predictor(BaseDummyPredictor):
    pass


class DummyPM10Predictor(BaseDummyPredictor):
    pass
