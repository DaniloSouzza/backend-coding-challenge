import re
import json
from dataclasses import dataclass
from .exceptions import InvalidPattern


@dataclass
class GistsHelper:

    gists: list
    pattern: str

    def __has_valid_patters(self, *, gist: dict):
        try:
            found_patterns = re.findall(self.pattern, json.dumps(gist))
            return any(found_patterns)
        except re.error:
            raise InvalidPattern("The inserted pattern is not valid.")

    def match_patterns(self):
        matches = []
        iter_gists = iter(self.gists)
        try:
            while gist := next(iter_gists):
                if self.__has_valid_patters(gist=gist):
                    matches.append(gist)
        except StopIteration:
            return matches
