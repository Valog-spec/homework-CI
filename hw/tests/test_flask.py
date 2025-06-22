import pytest

from hw.main.models import Parking


@pytest.mark.parametrize("route", ["/clients", "/clients/1"])
def test_route_status(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client, sample_client):
    assert sample_client.status_code == 201
    assert sample_client.json["id"] == 2
    assert sample_client.json["name"] == "Vova"


def test_create_parking(client, sample_parking):
    assert sample_parking.status_code == 201
    assert sample_parking.json["address"] == "Gagarina"
    assert sample_parking.json["id"] == 2


@pytest.mark.parking
def test_in_parking_space(client, db, sample_client, sample_parking):
    client_parking = {
        "client_id": sample_client.json["id"],
        "parking_id": sample_parking.json["id"],
    }

    park = db.session.get(Parking, sample_parking.json["id"])

    response = client.post("/client_parking", json=client_parking)

    assert park.count_available_places == 75
    assert sample_parking.json["count_available_places"] == 76
    assert response.json["time_in"] is not None
    assert response.json["time_out"] is None
    assert response.status_code == 201


@pytest.mark.parking
def test_out_parking_space(client, db, sample_client, sample_parking):
    client_parking = {
        "client_id": sample_client.json["id"],
        "parking_id": sample_parking.json["id"],
    }

    client.post("/client_parking", json=client_parking)

    park = db.session.get(Parking, sample_parking.json["id"])

    response = client.delete("/client_parking", json=client_parking)

    assert park.count_available_places == 76
    assert sample_client.json["car_number"] is not None
    assert sample_parking.json["opened"]
    assert response.status_code == 201
    assert response.json["time_in"] < response.json["time_out"]
