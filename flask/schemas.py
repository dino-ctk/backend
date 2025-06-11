from marshmallow import Schema, fields


class ItemScheme(Schema):
    id = fields.Str(dump_only=True) 
    name = fields.Str(required=True)
    price = fields.Int(required=True)
    store_id = fields.Str(required=True)

class ItemUpdateScheme(Schema):
    name = fields.Str(required=True)
    price = fields.Int(required=True)

class StoreScheme(Schema):
    id = fields.Str(dump_only=True) 
    name = fields.Str(required=True)  
