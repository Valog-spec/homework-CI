from flask import Flask, request
from marshmallow.validate import ValidationError
from hw.main.models import (
    Client,
    add_client,
    add_park,
    client_delete_parking,
    client_try_parking,
    db,
    get_client,
)
from hw.main.schemas import (
    ClientParkingSchema,
    ClientSchema,
    ParkingSchema,
)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///park.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=["GET", "POST"])
    def get_all_clients_and_add_client():
        if request.method == "GET":
            clients = Client.query.all()

            schema = ClientSchema()

            return schema.dump(clients, many=True)
        elif request.method == "POST":
            data = request.json
            schema = ClientSchema()
            try:
                client = schema.load(data)
            except ValidationError as exc:
                return exc.messages, 400

            client = add_client(client)
            return schema.dump(client), 201
        return None

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def client_get_by_id(client_id):
        client = get_client(client_id)
        schema = ClientSchema()
        return schema.dump(client)

    @app.route("/parking", methods=["POST"])
    def add_parking():
        data = request.json
        schema = ParkingSchema()
        try:
            parking = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        parking = add_park(parking)

        return schema.dump(parking), 201

    @app.route("/client_parking", methods=["POST", "DELETE"])
    def parking():
        if request.method == "POST":
            data = request.json
            schema = ClientParkingSchema()
            try:
                park = schema.load(data)
            except ValidationError as exc:
                return exc.messages, 400
            park = client_try_parking(park)
            return park, 201

        elif request.method == "DELETE":
            schema = ClientParkingSchema()
            data = request.json
            try:
                park = schema.load(data)
            except ValidationError as exc:
                return exc.messages, 400
            park = client_delete_parking(park)
            return schema.dump(park), 201

        return None

    return app
