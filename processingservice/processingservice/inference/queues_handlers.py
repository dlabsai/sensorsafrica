from typing import Any, Callable, Dict

from .process import process


def get_handlers() -> Dict[str, Callable[[Dict[str, Any]], bool]]:
    return {
        "make_inference": process,
    }
