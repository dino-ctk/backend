from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "Brodokomerc",
        "items": [
            {
                "name": "laksativ",
                "price": 10
            }
        ]
    }
]

@app.get("/stores")
def get_stores():
    return {"stores":stores}

@app.post("/stores")
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items":[]
    }
    stores.append(new_store)
    return new_store, 201

@app.post("/stores/<string:store_name>/item")
def create_item_in_store(store_name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == store_name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 401    
