from marshmallow import Schema, fields

class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    credit_card = fields.Str()
    car_number = fields.Str()


class ParkingSchema(Schema):
    id = fields.Int(dump_only=True)
    address = fields.Str(required=True)
    opened = fields.Boolean()
    count_places = fields.Int(required=True)
    count_available_places = fields.Int(required=True)


class ClientParkingSchema(Schema):
    id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    parking_id = fields.Int(required=True)
    time_in = fields.DateTime()
    time_out = fields.DateTime()

    # @validates_schema
    # def validate_ids(self, data, **kwargs):
    #     if 'client_id' in data:
    #         if not search_client(data["client_id"]):
    #             print("hi")
    #             raise ValidationError(f"Клиента с id: {data["client_id"]} нет")
