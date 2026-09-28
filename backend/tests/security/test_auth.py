def test_register_login_refresh_and_logout(client):
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "email": "auth-flow@example.com",
            "password": "Password123",
            "full_name": "Auth Flow",
            "organization_name": "Auth Flow Org",
        },
    )
    assert registration.status_code == 201, registration.text

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "auth-flow@example.com", "password": "Password123"},
    )
    assert login.status_code == 200, login.text
    refresh_token = login.json()["refresh_token"]

    refreshed = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refreshed.status_code == 200, refreshed.text
    assert refreshed.json()["access_token"]

    logout = client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert logout.status_code == 200
    rejected = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert rejected.status_code == 401


def test_authenticated_user_can_access_me(client):
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@example.com",
            "password": "Password123",
            "full_name": "Me",
            "organization_name": "Me Org",
        },
    )
    token = registration.json()["access_token"]
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
