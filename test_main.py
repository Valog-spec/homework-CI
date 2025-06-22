from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)


def test_add_recipe() -> None:
    response = client.post(
        url="/recipes",
        json={
            "name": "some",
            "cooking_time": 1,
            "description": "string",
            "ingredients": "string",
        },
    )
    assert response.status_code == 200


def test_add_wrong_recipe() -> None:
    response = client.post(
        url="/recipes",
        json={
            "name": "some",
            "cooking_time": "one",
            "description": "string",
            "ingredients": "string",
        },
    )

    assert response.status_code == 422
