from flask import Flask, request, jsonify
from flask.views import MethodView
from db import db
from sqlalchemy.exc import SQLAlchemyError
import uuid
from flask_smorest import abort, Blueprint
from schemas import StoreScheme, TagScheme

from models import TagModel, StoreModel, ItemModel

blp = Blueprint("Tags", __name__, description="Operations on tags")

@blp.route("/stores/<int:item_id>/tags/<int:tag_id>")
class Store(MethodView):
    @blp.response(201, TagScheme)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit() 
        except SQLAlchemyError:
                abort(500, message="An error occured while inserting the tag")  
        return tag 

    def delete(self, item_id, tag_id):   
        item = StoreModel.query.get_or_404(item_id)
        tag = StoreModel.query.get_or_404(tag_id)    

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit() 
        except SQLAlchemyError:
                abort(500, message="An error occured while inserting the tag")  
        return {"message":"Tag deleted from item"}


@blp.route("/stores/<int:store_id>/tags")
class Store(MethodView):
    @blp.response(200, TagScheme(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagScheme)
    @blp.response(201, TagScheme)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(
             TagModel.store_id == store_id,
             TagModel.name == tag_data["name"]
        ).first():
             abort(400, message="A tag with that name already exists in that store")

        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit() 
        except SQLAlchemyError:
                abort(500, message="An error occured while inserting the tag")  
        return tag  
    

@blp.route("/tags")
class TagList(MethodView):
    @blp.arguments(TagScheme)
    @blp.response(201, TagScheme)    
    def post(self, tag_data):
        tag = TagModel(**tag_data)
        try:
            db.session.add(tag)
            db.session.commit() 
        except SQLAlchemyError:
                abort(500, message="An error occured while inserting the store") 
        return tag        

@blp.route("/tags/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagScheme)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    def delete(self, tag_id):   
        tag = TagModel.query.get_or_404(tag_id)    
        db.session.delete(tag)
        db.session.commit()
        return {"message":"Tag deleted"}
