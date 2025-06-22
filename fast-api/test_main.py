from fastapi.testclient import TestClient
from main import app

client = TestClient(app=app)


def test_add_recipe():
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


def test_add_wrong_recipe():
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


# @pytest.mark.anyio
# async def test_add_recipe():
#     async with AsyncClient(transport=ASGITransport(app=app),
#                            base_url="http://") as ac:
#         response = await ac.post("/recipes", json={
#                               "name": "some",
#                               "cooking_time": 1,
#                               "description": "string",
#                               "ingredients": "string"}
#                             )
#         assert response.status_code == 200
