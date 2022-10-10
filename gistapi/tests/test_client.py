import json
import pytest
from gistapi import app


@pytest.fixture
def app_client():
    app.testing = True
    return app.test_client()


def test_ping_api(app_client):
    response = app_client.get("/ping")
    assert response.status_code == 200
    assert b"pong" in response.data


def test_get_on_seach_endpoint(app_client):
    response = app_client.get('/api/v1/search"')
    assert response.status_code == 404


def test_post_user_to_search_api_with_no_pattern(app_client):
    response = app_client.post(
        "/api/v1/search", json={"username": "justdionysus"}
    ).data.decode("utf-8")
    response_dict = json.loads(response)
    assert response_dict["error"] == "No pattern found on payload."


def test_post_user_to_search_api_with_no_username(app_client):
    response = app_client.post("/api/v1/search", json={}).data.decode("utf-8")
    response_dict = json.loads(response)
    assert response_dict["error"] == "No username found on payload."


def test_post_user_to_search_api_with_invalid_user(app_client):
    response = app_client.post(
        "/api/v1/search", json={"username": "!!!KKK", "pattern": ""}
    ).data.decode("utf-8")

    response_dict = json.loads(response)
    assert response_dict["error"] == "Not Found"


def test_post_user_to_search_api_with_data(app_client):
    response = app_client.post(
        "/api/v1/search",
        json={"username": "justdionysus", "pattern": "\\w\\.py"},
    ).data.decode("utf-8")

    response_dict = json.loads(response)
    assert len(response_dict["matches"]) == 2
