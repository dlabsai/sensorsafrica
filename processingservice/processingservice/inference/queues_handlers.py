import json

from typing import Any, Callable, Dict
from ..awsadapters.db import update_dynamodb_item

from .enums import InferenceStatus


def get_handlers() -> Dict[str, Callable[[Dict[str, Any]], bool]]:
    return {
        "make_inference": make_inference,
    }


def make_inference(payload: Dict[str, Any]) -> bool:
    # Load file from S3

    # Make inference

    # Save inference to S3

    # Update record in DynamoDB
    update_dynamodb_item(table_name="sensorsafrica-requests",
                         key={"RequestID": payload["RequestID"]},
                         update_expression="SET #status = :status",
                         expression_attribute_values={":status": InferenceStatus.SUCCESS.value},
                         expression_attribute_names={"#status": "Status"}
                         )

    return False  # TODO: change to True after testing
