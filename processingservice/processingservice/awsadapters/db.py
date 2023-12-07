from typing import Dict
import boto3
from .config import STANDARD


def get_dynamodb_table(table_name: str):
    # Connect to the DynamoDB service
    dynamodb = boto3.resource("dynamodb", config=STANDARD)

    # Connect to the specific table
    table = dynamodb.Table(table_name)

    return table


def update_dynamodb_item(
    *,
    table_name: str,
    key: Dict[str, str],
    update_expression: str,
    expression_attribute_values: Dict[str, str],
    expression_attribute_names: Dict[str, str] = None
):
    table = get_dynamodb_table(table_name)

    # Update the item
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names,
        ReturnValues="UPDATED_NEW",
    )

    return response
