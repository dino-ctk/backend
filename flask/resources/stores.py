from flask import Flask, request, jsonify
from flask.views import MethodView
from db import stores
import uuid
from flask_smorest import abort, Blueprint
from schemas import StoreScheme

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/stores")
class StoreList(MethodView):
    @blp.response(200, StoreScheme(many=True))
    def get(self):
        return stores.values()
    
    @blp.arguments(StoreScheme)
    @blp.response(201, StoreScheme)
    # Flask-Smorest injects the parsed and validated data as an argument to your method.
    def post(self, store_data):
        store_id = uuid.uuid4().hex
        new_store = {
            "id": store_id,
            **store_data
        }
        stores[store_id] = new_store
        return new_store

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreScheme)
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