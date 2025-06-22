from datetime import timedelta

import pytest
import datetime

from hw.main.models import db as _db, Client, ClientParking, Parking
from hw.main.flaskr.app import create_app


@pytest.fixture
def app():

    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        client = Client(
            id=1,
            name="Vova",
            surname="Petrov",
            credit_card="12345",
            car_number="NV123V999",
        )

        parking = Parking(
            id=1,
            address="Gagarina",
            opened=True,
            count_places=100,
            count_available_places=76,
        )

        client_parking = ClientParking(
            client_id=1,
            parking_id=1,
            time_in=datetime.datetime.now(datetime.UTC),
            time_out=datetime.datetime.now(datetime.UTC) + timedelta(hours=3),
        )
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app

        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db


@pytest.fixture
def sample_client(client):
    client_data = {
        "name": "Vova",
        "surname": "Petrov",
        "credit_card": "12345",
        "car_number": "NV123V999",
    }
    response = client.post("/clients", json=client_data)

    return response


@pytest.fixture
def sample_parking(client):
    parking_date = {
        "address": "Gagarina",
        "opened": True,
        "count_places": 10,
        "count_available_places": 76,
    }
    response = client.post("/parking", json=parking_date)

    return response
