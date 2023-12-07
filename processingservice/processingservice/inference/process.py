import pandas as pd
import logging

from typing import Any, Dict
from ..awsadapters.db import update_dynamodb_item
from ..data.transforms.dataset import build_input_records_for_inference, get_datasets

from .enums import InferenceStatus
from .loaders import load_user_uploaded_data_from_storage, load_predictors

logger = logging.getLogger(__name__)


def process(payload: Dict[str, Any]) -> bool:
    request_id = payload["RequestID"]
    # Load file from S3
    try:
        frame_with_data = load_user_uploaded_data_from_storage(payload["S3location"])
    except Exception as e:
        logger.error(f"Failed to load file from S3 for request ID {request_id} : {str(e)}")
        update_record_status(request_id, InferenceStatus.FAILED)
        return True

    # Build input records
    try:
        input_records = build_input_records_for_inference(csv_as_df=frame_with_data)
    except Exception as e:
        logger.error(f"Failed to build input records for request ID {request_id} : {str(e)}")
        update_record_status(request_id, InferenceStatus.FAILED)
        return True
    dataset_for_inference = get_datasets(input_records)

    # Make inference
    try:
        result = run_inference(*dataset_for_inference)
    except Exception as e:
        logger.error(f"Failed to run inference for request ID {request_id} : {str(e)}")
        update_record_status(request_id, InferenceStatus.FAILED)
        return True

    # Save inference to S3
    print(result)

    # Update DynamoDB record
    update_record_status(payload["RequestID"], InferenceStatus.SUCCESS)

    return False  # TODO: change to True after testing


def update_record_status(request_id: str, status: InferenceStatus) -> None:
    # Update record in DynamoDB
    update_dynamodb_item(table_name="sensorsafrica-requests",
                         key={"RequestID": request_id},
                         update_expression="SET #status = :status",
                         expression_attribute_values={":status": status.value},
                         expression_attribute_names={"#status": "Status"}
                         )


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
