from flask import Flask, request, jsonify
from flask.views import MethodView
from db import db
from sqlalchemy.exc import SQLAlchemyError
import uuid
from flask_smorest import abort, Blueprint
from schemas import ItemScheme, ItemUpdateScheme

from models import ItemModel

blp = Blueprint("items", "items", description="Operations on items")

@blp.route("/items")
class ItemList(MethodView):
    @blp.response(200, ItemScheme(many=True))
    def get(self):
        return ItemModel.query.all()
    
    # uvijek argumenti moraju biti iznad responsa
    @blp.arguments(ItemScheme)
    @blp.response(201, ItemScheme)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit() 
        except SQLAlchemyError:
                abort(500, message="An error occured while inserting the item")  
        return item          


@blp.route("/items/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemScheme)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(ItemUpdateScheme)
    @blp.response(201, ItemScheme)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
            item.store_id = item_data["store_id"]
            db.session.add(item)
            db.session.commit() 
                
        return item


    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item deleted"}


