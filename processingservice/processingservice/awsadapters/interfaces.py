from typing import Any, Dict

from humps import pascalize
from pydantic import BaseModel


def to_camel(string: str) -> str:
    return pascalize(string)


class MessageAttributes(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    handler_name: str


class Message(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    def to_payload(self, **kwargs: Any) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)

    request_id: str
    message_attributes: MessageAttributes
