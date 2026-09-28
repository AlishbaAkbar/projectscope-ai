from concurrent.futures import ThreadPoolExecutor


def test_ten_concurrent_project_creates_succeed(client, auth_headers):
    def create_project(index):
        return client.post(
            "/api/v1/projects",
            headers=auth_headers,
            json={
                "name": f"Concurrent Project {index}",
                "description": f"Project description number {index} for load verification.",
            },
        )

    with ThreadPoolExecutor(max_workers=10) as pool:
        responses = list(pool.map(create_project, range(10)))
    assert all(response.status_code == 201 for response in responses)
    assert len({response.json()["id"] for response in responses}) == 10
