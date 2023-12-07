import pandas as pd
from abc import abstractmethod


class BasePredictor:
    @abstractmethod
    def predict(self, data: pd.DataFrame):
        pass
