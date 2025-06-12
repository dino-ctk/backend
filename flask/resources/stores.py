from flask import Flask, request, jsonify
from flask.views import MethodView
from db import db
from sqlalchemy.exc import SQLAlchemyError
import uuid
from flask_smorest import abort, Blueprint
from schemas import StoreScheme

from models import StoreModel

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/stores")
class StoreList(MethodView):
    @blp.response(200, StoreScheme(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreScheme)
    @blp.response(201, StoreScheme)
    # Flask-Smorest injects the parsed and validated data as an argument to your method.
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit() 
        except SQLAlchemyError:
                abort(500, message="An error occured while inserting the store") 
        return store        

@blp.route("/stores/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreScheme)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Item deleted"}