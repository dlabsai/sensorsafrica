import json
import os
from typing import Dict

from botocore import exceptions
from logging import getLogger

from .interfaces import Message
from .utils import get_queue, get_sqs_client

logger = getLogger(__name__)


def send_generic_message(
    msg_body: Message,
    queue_name: str,
) -> bool:
    """
    Send a message to a provided queue.
    :param msg_body: Message object containing at least:
        requestId = request message ID
    :param queue_name: a queue (by name) to which the message should be sent
    :return: None
    """
    if os.environ.get("TEST_BUILD"):
        return True

    payload = msg_body.dict()
    message_attributes = build_string_message_attributes(
        payload.pop("message_attributes", {})
    )
    message_body = json.dumps(payload)
    try:
        response = get_sqs_client().send_message(
            QueueUrl=get_queue(queue_name),
            MessageBody=message_body,
            MessageAttributes=message_attributes,
        )
    except exceptions.ClientError as error:
        logger.warning(f"AWS SQS sender: {str(error)} for queue {queue_name}")
        return False

    logger.info(
        f"AWS SQS sender: {response['MessageId']} for queue {queue_name}",
    )
    return True


def build_string_message_attributes(
    message_attributes: Dict[str, str]
) -> Dict[str, Dict[str, str]]:
    return {
        key: {"StringValue": value, "DataType": "String"}
        for key, value in message_attributes.items()
    }
