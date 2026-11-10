API = "/api/tasks/"


def create(client, **data):
    data.setdefault("title", "Minha tarefa")
    return client.post(API, json=data)


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_index_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Task Manager" in response.data


def test_list_empty(client):
    response = client.get(API)

    assert response.status_code == 200
    assert response.json == []


def test_create_task(client):
    response = create(client, title="Estudar Flask", description="Capítulo 1")

    assert response.status_code == 201
    assert response.json == {
        "id": 1,
        "title": "Estudar Flask",
        "description": "Capítulo 1",
        "completed": False,
    }


def test_create_without_description(client):
    response = create(client)

    assert response.status_code == 201
    assert response.json["description"] is None


def test_create_validation_error(client):
    response = create(client, title="ab")

    assert response.status_code == 400
    assert response.json["error"] == "Validation error"


def test_create_missing_title(client):
    response = client.post(API, json={"description": "sem título"})

    assert response.status_code == 400


def test_list_returns_newest_first(client):
    create(client, title="Primeira")
    create(client, title="Segunda")

    titles = [t["title"] for t in client.get(API).json]

    assert titles == ["Segunda", "Primeira"]


def test_get_task(client):
    task_id = create(client).json["id"]

    response = client.get(f"{API}{task_id}")

    assert response.status_code == 200
    assert response.json["id"] == task_id


def test_get_task_not_found(client):
    response = client.get(f"{API}999")

    assert response.status_code == 404


def test_update_task_partial(client):
    task_id = create(client, description="original").json["id"]

    response = client.patch(f"{API}{task_id}", json={"completed": True})

    assert response.status_code == 200
    assert response.json["completed"] is True
    assert response.json["title"] == "Minha tarefa"
    assert response.json["description"] == "original"


def test_update_can_clear_description(client):
    task_id = create(client, description="original").json["id"]

    response = client.patch(f"{API}{task_id}", json={"description": None})

    assert response.json["description"] is None


def test_update_validation_error(client):
    task_id = create(client).json["id"]

    response = client.patch(f"{API}{task_id}", json={"title": "ab"})

    assert response.status_code == 400


def test_update_not_found(client):
    response = client.patch(f"{API}999", json={"completed": True})

    assert response.status_code == 404


def test_delete_task(client):
    task_id = create(client).json["id"]

    response = client.delete(f"{API}{task_id}")

    assert response.status_code == 200
    assert client.get(f"{API}{task_id}").status_code == 404


def test_delete_not_found(client):
    response = client.delete(f"{API}999")

    assert response.status_code == 404
