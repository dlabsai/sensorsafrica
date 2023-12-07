import pandas as pd

from typing import Any, Dict
from ..awsadapters.db import update_dynamodb_item
from ..data.transforms.dataset import build_input_records, get_datasets

from .enums import InferenceStatus
from .loaders import load_user_uploaded_data_from_storage, load_predictors


def process(payload: Dict[str, Any]) -> bool:
    # Load file from S3
    frame_with_data = load_user_uploaded_data_from_storage(payload["S3location"])

    input_records = build_input_records(csv_as_df=frame_with_data)
    dataset_for_inference = get_datasets(input_records)

    # Make inference
    result = run_inference(*dataset_for_inference)

    # Save inference to S3
    print(result)

    # Update record in DynamoDB
    update_dynamodb_item(table_name="sensorsafrica-requests",
                         key={"RequestID": payload["RequestID"]},
                         update_expression="SET #status = :status",
                         expression_attribute_values={":status": InferenceStatus.SUCCESS.value},
                         expression_attribute_names={"#status": "Status"}
                         )

    return False  # TODO: change to True after testing


def run_inference(df_pm_1: pd.DataFrame, df_pm_2_5: pd.DataFrame, df_pm_10: pd.DataFrame) -> pd.DataFrame:
    df_pred_pm_1 = df_pm_1[df_pm_1['value'].isnull()]
    df_pred_pm_2_5 = df_pm_2_5[df_pm_2_5['value'].isnull()]
    df_pred_pm_10 = df_pm_10[df_pm_10['value'].isnull()]

    pm_1_predictor, pm_2_5_predictor, pm_10_predictor = load_predictors()

    df_pred_pm_1['value'] = pm_1_predictor.predict(df_pred_pm_1)
    df_pred_pm_2_5['value'] = pm_2_5_predictor.predict(df_pred_pm_2_5)
    df_pred_pm_10['value'] = pm_10_predictor.predict(df_pred_pm_10)

    result = pd.concat([df_pred_pm_1, df_pred_pm_2_5, df_pred_pm_10], ignore_index=True)

    return result
