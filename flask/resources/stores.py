from flask import Flask, request, jsonify
from flask.views import MethodView
from db import stores
import uuid
from flask_smorest import abort, Blueprint

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/stores")
class StoreList(MethodView):
    def get(self):
        return {"stores":list(stores.values())}
    
    def post(self):
        stores_data = request.get_json()
        store_id = uuid.uuid4().hex
        new_store = {
            "id": store_id,
            **stores_data
        }
        stores[store_id] = new_store
        return jsonify(new_store), 201

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return jsonify(stores[store_id])
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return jsonify({"message":"store deleted"})
        except KeyError:
            abort(404, message="Store not foundd") 