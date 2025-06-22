from hw.main.models import Client, Parking
from hw.tests.factories import ClientFactory, ParkingFactory

def test_create_client(app, db):
    user = ClientFactory()
    db.session.commit()
    assert user.id is not None
    assert len(db.session.query(Client).all()) == 2


def test_create_parking(client, db):
    product = ParkingFactory()
    db.session.commit()
    assert product.id is not None
    assert len(db.session.query(Parking).all()) == 2