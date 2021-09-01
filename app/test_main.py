from os import environ
from fastapi.testclient import TestClient

from .auth0 import Auth0User
from .main import app, auth
from .database.db import get_db
from .database.mock_db import override_get_db
from .database.schemas import User


def override_get_auth_user():
    return Auth0User(sub="1")


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[auth.get_user] = override_get_auth_user

client = TestClient(app)


def test_add_user():
    response = client.post(
        "/users/",
        headers={"Authorization": "bearer abc123"},
        json={"email": "test@email.co", "id": "1"},
    )
    assert response.status_code == 200
    assert response.json() == User(id="1")


# def test_read_item_bad_token():
#     response = client.get("/items/foo", headers={"x-token": "hailhydra"})
#     assert response.status_code == 400
#     assert response.json() == {"detail": "invalid x-token header"}


# def test_read_inexistent_item():
#     response = client.get("/items/baz", headers={"x-token": "coneofsilence"})
#     assert response.status_code == 404
#     assert response.json() == {"detail": "item not found"}


# def test_create_item():
#     response = client.post(
#         "/items/",
#         headers={"x-token": "coneofsilence"},
#         json={"id": "foobar", "title": "foo bar", "description": "the foo barters"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": "foobar",
#         "title": "foo bar",
#         "description": "the foo barters",
#     }


# def test_create_item_bad_token():
#     response = client.post(
#         "/items/",
#         headers={"x-token": "hailhydra"},
#         json={"id": "bazz", "title": "bazz", "description": "drop the bazz"},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "invalid x-token header"}


# def test_create_existing_item():
#     response = client.post(
#         "/items/",
#         headers={"x-token": "coneofsilence"},
#         json={
#             "id": "foo",
#             "title": "the foo id stealers",
#             "description": "there goes my stealer",
#         },
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "item already exists"}
