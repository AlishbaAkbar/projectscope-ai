from app.core.rate_limit import limiter


def test_login_is_rate_limited_after_five_attempts(client):
    limiter.reset()
    try:
        responses = [
            client.post(
                "/api/v1/auth/login",
                json={"email": "nobody@example.com", "password": "WrongPassword1"},
            )
            for _ in range(6)
        ]
        assert all(response.status_code == 401 for response in responses[:5])
        assert responses[5].status_code == 429
    finally:
        limiter.reset()
