from flask import Flask, request, jsonify
from flask.views import MethodView
from db import items, stores
import uuid
from flask_smorest import abort, Blueprint


blp = Blueprint("items", "items", description="Operations on items")

@blp.route("/items")
class ItemList(MethodView):
    def get(self):
        return jsonify({"items":list(items.values())})
    
    def post(self):
        item_data = request.get_json()
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
        return jsonify(new_Item), 201


@blp.route("/items/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return jsonify(items[item_id])
        except KeyError:
            abort(404, message="Item not foundd")

    def put(self, item_id):
        item_data = request.get_json()

        if "price" not in item_data or "name" not in item_data:
            abort(
                400,
                message = "Bad request. price and name are required"
            )

        try:
            item = items[item_id]
            item |= item_data
            return jsonify(item)
        except KeyError:
            abort(404, message="Item not foundd")            

    def delete(self, item_id):
        try:
            del items[item_id]
            return jsonify({"message":"item deleted"})
        except KeyError:
            abort(404, message="Item not foundd")
