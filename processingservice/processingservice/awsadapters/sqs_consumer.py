from typing import Any, Optional

import json
import boto3

from logging import getLogger
from .common import SignalHandler
from .config import STANDARD

logger = getLogger(__name__)

sqs = boto3.resource("sqs", config=STANDARD)


def get_attribute_value(sqs_message: Any, attr_key: str) -> Optional[str]:
    if not sqs_message.message_attributes:
        return None
    attribute = sqs_message.message_attributes.get(attr_key, {})
    if attribute.get("DataType", "") == "String":
        return attribute.get("StringValue", "")
    else:
        return None


def message_dispatcher(sqs_message: Any, queues_handlers: Any) -> bool:
    # We have only one handler for now, so let us hardcode it
    handler_name = get_attribute_value(sqs_message, "handler_name") or "make_inference"

    return queues_handlers[handler_name](json.loads(sqs_message.body))


def consume_messages(queue_name: str, queues_handlers: Any) -> None:
    logger.info("AWS SQS consumer: Consuming messages for queue {queue_name}")
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    signal_handler = SignalHandler()
    while not signal_handler.received_signal:
        messages = queue.receive_messages(
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1,
            VisibilityTimeout=10
            * 2,  # number of messages times forecasted time of executing
            # one message (magic number)
            MessageAttributeNames=["handler_name", "username"],
        )
        for message in messages:
            logger.info(f"AWS SQS consumer processing message {message.message_id}")
            try:
                has_dispatched = message_dispatcher(message, queues_handlers)
                if has_dispatched:
                    logger.info(
                        f"AWS SQS consumer deleting message {message.message_id}"
                    )
                    message.delete()
                    logger.info(
                        f"AWS SQS consumer message deleted {message.message_id}"
                    )
                else:
                    logger.warning(
                        f"AWS SQS consumer dispatch failed {message.message_id}"
                    )
            except AssertionError as e:
                logger.warning(
                    f"AWS SQS consumer; {queue_name}, {message.message_id}, msg={str(e)}"
                )
            except Exception as e:
                logger.warning(
                    f"AWS SQS consumer; {queue_name}, {message.message_id}, {str(e)}"
                )
