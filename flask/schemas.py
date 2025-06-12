from marshmallow import Schema, fields


class PlainItemScheme(Schema):
    id = fields.Int(dump_only=True) 
    name = fields.Str(required=True)
    price = fields.Int(required=True)

class PlainStoreScheme(Schema):
    id = fields.Int(dump_only=True) 
    name = fields.Str(required=True) 

class PlainTagScheme(Schema):
    id = fields.Int(dump_only=True) 
    name = fields.Str(required=True)   

class ItemScheme(PlainItemScheme):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreScheme(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagScheme(), dump_only=True))
    
class ItemUpdateScheme(Schema):
    name = fields.Str(required=False)
    price = fields.Int(required=False)
    store_id = fields.Int(required=False)

class StoreScheme(PlainStoreScheme):
    items = fields.List(fields.Nested(PlainItemScheme(), dump_only=True))
    tags = fields.List(fields.Nested(PlainTagScheme(), dump_only=True))

class TagScheme(PlainTagScheme):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemScheme(), dump_only=True))
    store = fields.Nested(PlainStoreScheme(), dump_only=True)

class TagAndItemScheme(Schema):
    items = fields.Nested(ItemScheme)
    tag = fields.Nested(TagScheme)
