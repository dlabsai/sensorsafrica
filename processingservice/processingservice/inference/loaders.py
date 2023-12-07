from .dummy import DummyPM1Predictor, DummyPM25Predictor, DummyPM10Predictor


def load_predictors():
    return DummyPM1Predictor(), DummyPM25Predictor(), DummyPM10Predictor()
