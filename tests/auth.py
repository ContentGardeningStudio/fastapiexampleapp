from fastapi import FastAPI
from fastapi.testclient import TestClient


from src.auth import router as auth_router
from src.config import (
    DEBUG,
    PROJECT_NAME,
    API_VERSION,
)

# inited FastAPI app
app = FastAPI(
    title=f"{PROJECT_NAME} API",
    version=API_VERSION,
    debug=DEBUG,
)
app.include_router(auth_router.router)

client = TestClient(app)


def test_create_user():
    sample_payload = {
        "email": "test@example.com",
        "password": "pass123",
        "re_password": "pass123",
    }
    # Make a post request to the /register/ endpoint
    response = client.post("/register", json=sample_payload)

    # Check if the response status code is 201
    assert response.status_code == 201

    # Check if the response contains the expected keys and values
    expected_keys = ["id", "email", "is_active", "is_staff", "is_superuser"]
    assert all(key in response.json() for key in expected_keys)

    # Optionally, check if the ID is a non-empty string (assuming it's a string)
    assert response.json()["id"] != ""

    # You can also check if the ID is of the expected type, e.g., int or str
    assert isinstance(response.json()["id"], (int, str))

    # Check specific assertions for known values
    assert response.json()["email"] == sample_payload["email"]
    assert response.json()["is_active"] is True
    assert response.json()["is_staff"] is False
    assert response.json()["is_superuser"] is False


def test_read_users():
    # Make a request to the /users/ endpoint
    response = client.get("/users/")

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response contains the expected data
    expected_keys = ["id", "email", "is_active", "is_staff", "is_superuser"]
    for user in response.json():
        assert all(key in user for key in expected_keys)

    # Additional assertions based on your requirements
    # For example, you might want to check the length of the returned list
    assert len(response.json()) > 0
