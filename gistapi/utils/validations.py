from dataclasses import dataclass
from .exceptions import NoPatternInformed, NoUsernameInformed, UserNotFound


@dataclass
class PayloadValidator:

    payload: dict

    @property
    def __has_pattern(self):
        return "pattern" in self.payload

    @property
    def __has_username(self):
        return "username" in self.payload

    def validate_api_payload(self):
        if not self.__has_username:
            raise NoUsernameInformed("No username found on payload.")
        if not self.__has_pattern:
            raise NoPatternInformed("No pattern found on payload.")


@dataclass
class ResponseValidator:

    payload: dict

    @property
    def __has_error_message(self):
        return "message" in self.payload

    def validate_response(self):
        if self.__has_error_message:
            raise UserNotFound(self.payload["message"])
