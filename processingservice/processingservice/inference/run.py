import pandas as pd

from processingservice.inference.dummy import DummyPM1Predictor, DummyPM25Predictor, DummyPM10Predictor


def run_inference(df_pm_1, df_pm_2_5, df_pm_10) -> pd.DataFrame:
    df_pred_pm_1 = df_pm_1[df_pm_1['value'].isnull()]
    df_pred_pm_2_5 = df_pm_2_5[df_pm_2_5['value'].isnull()]
    df_pred_pm_10 = df_pm_10[df_pm_10['value'].isnull()]

    df_pred_pm_1['value'] = DummyPM1Predictor().predict(df_pred_pm_1)
    df_pred_pm_2_5['value'] = DummyPM25Predictor().predict(df_pred_pm_2_5)
    df_pred_pm_10['value'] = DummyPM10Predictor().predict(df_pred_pm_10)

    result = pd.concat([df_pred_pm_1, df_pred_pm_2_5, df_pred_pm_10], ignore_index=True)

    return result
