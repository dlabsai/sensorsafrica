import pandas as pd

from .loaders import load_predictors


def run_inference(df_pm_1, df_pm_2_5, df_pm_10) -> pd.DataFrame:
    df_pred_pm_1 = df_pm_1[df_pm_1['value'].isnull()]
    df_pred_pm_2_5 = df_pm_2_5[df_pm_2_5['value'].isnull()]
    df_pred_pm_10 = df_pm_10[df_pm_10['value'].isnull()]

    pm_1_predictor, pm_2_5_predictor, pm_10_predictor = load_predictors()

    df_pred_pm_1['value'] = pm_1_predictor.predict(df_pred_pm_1)
    df_pred_pm_2_5['value'] = pm_2_5_predictor.predict(df_pred_pm_2_5)
    df_pred_pm_10['value'] = pm_10_predictor.predict(df_pred_pm_10)

    result = pd.concat([df_pred_pm_1, df_pred_pm_2_5, df_pred_pm_10], ignore_index=True)

    return result
