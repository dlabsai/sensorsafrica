import boto3

from .config import STANDARD


def get_sqs_client():
    return boto3.client("sqs", config=STANDARD)


def get_queue(queue_name: str) -> str:
    # TODO: add errors handling etc
    return get_sqs_client().get_queue_url(QueueName=queue_name)["QueueUrl"]
