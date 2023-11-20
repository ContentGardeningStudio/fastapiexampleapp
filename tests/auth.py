from fastapi import FastAPI
from fastapi.testclient import TestClient
from faker import Faker


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

fake = Faker()
fake_email = fake.email()
fake_password = fake.password()


def test_create_user():
    sample_payload = {
        "email": fake_email,
        "password": fake_password,
        "re_password": fake_password,
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
    assert response.json()["email"] == fake_email
    assert response.json()["is_active"] is True
    assert response.json()["is_staff"] is False
    assert response.json()["is_superuser"] is False


def test_login_for_access_token():
    # we use the same fake email to tcheck login token
    login_data = {"username": fake_email, "password": fake_password}

    # Make a post request to the /token/ endpoint
    response = client.post("/token", data=login_data)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the token in respose body
    assert "access_token" in response.json() and response.json()["access_token"] != ""
    assert response.json()["token_type"] == "bearer"


def test_read_users_me():
    # Make a post request to the /token/ endpoint to obtain access token
    res = client.post(
        "/token", data={"username": fake_email, "password": fake_password}
    )

    # Check if the token in respose body
    assert res.status_code == 200
    access_token = res.json()["access_token"]

    # Add the token to the headers
    headers = {"Authorization": f"Bearer {access_token}"}

    # Make a request to the /users/me/ endpoint with the token in the headers
    response = client.get("/users/me", headers=headers)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response contains the expected keys and values
    expected_keys = ["id", "email", "is_active", "is_staff", "is_superuser"]
    assert all(key in response.json() for key in expected_keys)

    # Check specific assertions for known values
    assert response.json()["email"] == fake_email
    assert response.json()["is_active"] is True
    assert response.json()["is_staff"] is False
    assert response.json()["is_superuser"] is False


def test_read_users():
    # Make a request to the /users/ endpoint
    response = client.get("/users")

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response contains the expected data
    expected_keys = ["id", "email", "is_active", "is_staff", "is_superuser"]
    for user in response.json():
        assert all(key in user for key in expected_keys)

    # Additional assertions based on requirements
    # For example, check the length of users list
    assert len(response.json()) > 0
