def test_get_progress_requires_authentication(client, test_resource):
    response = client.get("/api/resources/progress")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required."


def test_put_progress_creates_entry(client, auth_headers, test_resource):
    response = client.put(
        f"/api/resources/{test_resource.id}/progress",
        headers=auth_headers,
        json={"status": "in_progress"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["resource_id"] == test_resource.id
    assert body["status"] == "in_progress"


def test_put_progress_updates_existing_entry(client, auth_headers, test_resource):
    first_response = client.put(
        f"/api/resources/{test_resource.id}/progress",
        headers=auth_headers,
        json={"status": "not_started"},
    )
    second_response = client.put(
        f"/api/resources/{test_resource.id}/progress",
        headers=auth_headers,
        json={"status": "completed"},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json()["id"] == second_response.json()["id"]
    assert second_response.json()["status"] == "completed"


def test_get_progress_returns_current_user_entries(client, auth_headers, test_resource):
    client.put(
        f"/api/resources/{test_resource.id}/progress",
        headers=auth_headers,
        json={"status": "completed"},
    )

    response = client.get("/api/resources/progress", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["resource_id"] == test_resource.id
    assert body[0]["status"] == "completed"


def test_put_progress_returns_404_for_missing_resource(client, auth_headers):
    response = client.put(
        "/api/resources/999999/progress",
        headers=auth_headers,
        json={"status": "in_progress"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Resource not found."


def test_delete_progress_removes_entry(client, auth_headers, test_resource):
    client.put(
        f"/api/resources/{test_resource.id}/progress",
        headers=auth_headers,
        json={"status": "in_progress"},
    )

    delete_response = client.delete(
        f"/api/resources/{test_resource.id}/progress",
        headers=auth_headers,
    )
    list_response = client.get("/api/resources/progress", headers=auth_headers)

    assert delete_response.status_code == 204
    assert list_response.status_code == 200
    assert list_response.json() == []
