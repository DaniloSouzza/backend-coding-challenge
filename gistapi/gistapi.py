"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import requests

from flask import Flask, Response, jsonify, request
from .utils.gists_helpers import GistsHelper
from .utils.validations import PayloadValidator, ResponseValidator
from .utils.exceptions import (
    NoPatternInformed,
    NoUsernameInformed,
    InvalidPattern,
    UserNotFound,
)


app = Flask(__name__)

API_EXCEPTIONS = (
    NoPatternInformed,
    NoUsernameInformed,
    UserNotFound,
    InvalidPattern,
)


@app.route("/ping")
def ping() -> str:
    """Provide a static response to a simple GET request."""
    return "pong"


def gists_for_user(username: str) -> dict:
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    gists_url = "https://api.github.com/users/{username}/gists".format(
        username=username
    )
    response = requests.get(gists_url)
    return response.json()


@app.route("/api/v1/search", methods=["POST"])
def search() -> Response:
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data: dict = request.get_json()
    result = {}
    try:
        validate_payload: PayloadValidator = PayloadValidator(post_data)
        validate_payload.validate_api_payload()

        username = post_data["username"]
        pattern = post_data["pattern"]

        gists: dict = gists_for_user(username)

        validate_response: ResponseValidator = ResponseValidator(gists)
        validate_response.validate_response()

        gists_helper = GistsHelper(gists=gists, pattern=pattern)
        matches = gists_helper.match_patterns()

        result["status"] = "success"
        result["username"] = username
        result["pattern"] = pattern
        result["matches"] = matches

    except API_EXCEPTIONS as exception:
        result["error"] = exception.args[0]
        result["status"] = "failed"

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9876)
