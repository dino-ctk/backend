from flask import Flask, request, jsonify
from flask.views import MethodView
from db import items, stores
import uuid
from flask_smorest import abort, Blueprint
from schemas import ItemScheme, ItemUpdateScheme


blp = Blueprint("items", "items", description="Operations on items")

@blp.route("/items")
class ItemList(MethodView):
    @blp.response(200, ItemScheme(many=True))
    def get(self):
        return jsonify({"items":list(items.values())})
    
    @blp.arguments(ItemScheme)
    @blp.response(201, ItemScheme)
    def post(self, item_data):
        store_id = item_data.get("store_id")
        if store_id not in stores:
            abort(404, message="Store not found")
        item_id = uuid.uuid4().hex
        new_Item = {
            "id": item_id,
            "store_id": store_id,
            ** item_data
        }

        items[item_id] = new_Item
        return new_Item


@blp.route("/items/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemScheme)
    def get(self, item_id):
        try:
            return jsonify(items[item_id])
        except KeyError:
            abort(404, message="Item not foundd")

    @blp.arguments(ItemUpdateScheme)
    @blp.response(201, ItemScheme)
    def put(self, item_id):
        item_data = request.get_json()
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not foundd")            

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message":"item deleted"}
        except KeyError:
            abort(404, message="Item not foundd")
