import time
from signal import SIGINT, SIGTERM, signal
from typing import Any, Dict

from logging import getLogger

logger = getLogger(__name__)


class SignalHandler:
    def __init__(self) -> None:
        self.received_signal = False
        signal(SIGINT, self._signal_handler)
        signal(SIGTERM, self._signal_handler)

    def _signal_handler(self, signal: Any, frame: Any) -> None:
        logger.info(f"handling signal {signal}, exiting gracefully")
        self.received_signal = True


def wait(seconds: int):
    def decorator(fun):
        last_run = time.monotonic()

        def new_fun(*args, **kwargs):
            nonlocal last_run
            now = time.monotonic()
            if time.monotonic() - last_run > seconds:
                last_run = now
                return fun(*args, **kwargs)

        return new_fun

    return decorator


def set_msg_string_attribute_value(value: str) -> Dict[str, str]:
    return {
        "DataType": "String",
        "StringValue": str(value),
    }  # just make sure value is a string
