from flask import Flask, request, jsonify
from db import stores, items
import uuid
from flask_smorest import abort

app = Flask(__name__)


### STORES

@app.get("/stores")
def get_stores():
    return jsonify({"stores": list(stores.values())})

@app.post("/stores")
def create_store():
    stores_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {
        "id": store_id,
        "name": stores_data["name"],
        "items":[]
    }
    stores[store_id] = new_store
    return jsonify(new_store), 201

@app.get("/stores/<string:store_id>")
def get_store(store_id):
    try:
        return jsonify(stores[store_id])
    except KeyError:
        abort(404, message="Store not found")
    

#### ITEMS    
@app.get("/items")
def get_all_items():
    return jsonify({"items":list(items.values())})

@app.get("/items/<string:item_id>")
def get_item(item_id):
    try:
        return jsonify(items[item_id])
    except KeyError:
        abort(404, message="Item not foundd")
    

        
@app.post("/items")
def create_item():
    item_data = request.get_json()
    store_id = item_data.get("store_id")
    if store_id not in stores:
        abort(404, message="Store not found")
    
    
    item_id = uuid.uuid4().hex
    new_Item = {
        "id": item_id,
        "name": item_data.get("name"),
        "price": item_data.get("price"),
        "store_id": store_id
    }

    items[item_id] = new_Item
    return jsonify(new_Item), 201
