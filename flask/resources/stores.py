from flask import Flask, request, jsonify
from flask.views import MethodView
from db import db
from sqlalchemy.exc import SQLAlchemyError
import uuid
from flask_smorest import abort, Blueprint
from schemas import StoreScheme
from flask_jwt_extended import jwt_required

from models import StoreModel, TagModel

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
        return {"message":"Store deleted"}
    
    @blp.arguments(StoreScheme)
    @blp.response(201, StoreScheme)
    def put(self, store_data, store_id):
        store = StoreModel.query.get_or_404(store_id)
        store.name = store_data.get("name", store.name)

        if "tags" in store_data:
            # Remove existing tags
            for tag in store.tags.all():
                db.session.delete(tag)
            # Create new TagModel from store_data
            for tag in store_data["tags"]:
                new_tag = TagModel(name=tag.get("name"), store_id=store.id)
                store.tags.append(new_tag)
            try:
                db.session.commit() 
            except SQLAlchemyError:
                    abort(500, message="An error occured while inserting the store") 
            return store           
