import factory
from factory.fuzzy import FuzzyChoice
from faker import Faker

from hw.main.models import Client, Parking, db

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = fake.credit_card_number()
    car_number = fake.bothify("??###?##", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = FuzzyChoice([True, False])
    count_places = factory.Faker("random_int", min=50, max=100)
    count_available_places = factory.Faker("random_int", min=30, max=50)
