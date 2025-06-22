from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import datetime

from hw.main.schemas import ClientParkingSchema

db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    parkings = db.relationship("ClientParking", back_populates="client")


class Parking(db.Model):
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    clients = db.relationship("ClientParking", back_populates="parking")


class ClientParking(db.Model):
    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    client = db.relationship("Client", back_populates="parkings")
    parking = db.relationship("Parking", back_populates="clients")

    __table_args__ = (
        db.UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )


def add_client(data):
    client = Client(**data)
    db.session.add(client)
    db.session.commit()

    return client


def get_client(idx):
    client = Client.query.filter(Client.id == idx).one()

    return client


def add_park(data):
    parking = Parking(**data)
    db.session.add(parking)
    db.session.commit()

    return parking


def search_client(idx):
    client = Client.query.filter(Client.id == idx).one()
    if client:
        return True
    return False


def client_try_parking(data):
    # client = Client.query.filter(Client.id == data["client_id"]).one()
    client = db.session.get(Client, data["client_id"] )
    # park = Parking.query.filter(Parking.id == data["parking_id"]).one()
    park = db.session.get(Parking, data["parking_id"])
    if not client:
        return {"message": "Вас нет в базу данных"}
    elif not park:
        return {"message": "Такой парковки не сущетсвует"}
    elif client.credit_card is None:
        return {"message": "К сожелению вы не можете заехать на парковку так как вы не привезали банковскую карту"}
    elif park.count_available_places > 0 and park.opened == True:
        park.count_available_places -= 1
        client_parking = ClientParking(client_id=data["client_id"], parking_id=data["parking_id"],
                                       time_in=datetime.datetime.now(datetime.UTC),
                                       )
        db.session.add(client_parking)

        try:
            db.session.commit()
        except IntegrityError:
            return {"message": "Такой клиет уже есть"}
        schema = ClientParkingSchema()
        return schema.dump(client_parking)
    else:
        return {"message": "Парковка закрыта"}


def client_delete_parking(data):
    client = db.session.get(Client, data["client_id"])
    park = db.session.get(Parking, data["parking_id"])
    client_parking = ClientParking.query.filter(ClientParking.client_id == client.id,
                                                ClientParking.parking_id == park.id).one()
    if client_parking:
        park.count_available_places += 1
        client_parking.time_out = datetime.datetime.now(datetime.UTC)
        db.session.commit()
        return client_parking
    return "Не верные данные"




