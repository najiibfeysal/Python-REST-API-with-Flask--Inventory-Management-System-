from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


# MOCK DATABASE
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "ingredients": "Filtered water, almonds, cane sugar",
        "price": 5.99,
        "stock": 20
    },
    {
        "id": 2,
        "product_name": "Nutella",
        "brand": "Ferrero",
        "ingredients": "Sugar, palm oil, hazelnuts, cocoa",
        "price": 7.99,
        "stock": 15
    }
]


# HELPER FUNCTION
def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item

    return None


# GET ALL INVENTORY
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


# GET ONE INVENTORY ITEM
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):

    item = find_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    return jsonify(item), 200


# CREATE INVENTORY ITEM
@app.route("/inventory", methods=["POST"])
def create_item():

    data = request.get_json() or {}

    if "product_name" not in data:
        return jsonify({
            "error": "product_name is required"
        }), 400

    if "price" not in data:
        return jsonify({
            "error": "price is required"
        }), 400

    if "stock" not in data:
        return jsonify({
            "error": "stock is required"
        }), 400

    new_id = max(
        [item["id"] for item in inventory],
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "product_name": data["product_name"],
        "brand": data.get("brand", ""),
        "ingredients": data.get("ingredients", ""),
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


# UPDATE INVENTORY ITEM
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):

    item = find_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    data = request.get_json() or {}

    allowed_fields = [
        "product_name",
        "brand",
        "ingredients",
        "price",
        "stock"
    ]

    for field in allowed_fields:
        if field in data:
            item[field] = data[field]

    return jsonify(item), 200


# DELETE INVENTORY ITEM
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):

    item = find_item(item_id)

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    inventory.remove(item)

    return jsonify({
        "message": "Inventory item deleted successfully"
    }), 200


# OPEN FOOD FACTS API
def fetch_product_from_openfoodfacts(product_name):

    url = "https://world.openfoodfacts.org/api/v2/search"

    params = {
        "search_terms": product_name,
        "page_size": 1,
        "fields": (
            "product_name,"
            "brands,"
            "ingredients_text,"
            "categories,"
            "image_url"
        )
    }

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        print(
            "Open Food Facts status:",
            response.status_code
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        print(
            "Open Food Facts API error:",
            repr(error)
        )

        return None


# GET PRODUCT FROM OPEN FOOD FACTS
@app.route("/api/product/<path:product_name>", methods=["GET"])
def get_external_product(product_name):

    data = fetch_product_from_openfoodfacts(product_name)

    if data is None:
        return jsonify({
            "error": "Open Food Facts is currently unavailable"
        }), 503

    products = data.get("products", [])

    if not products:
        return jsonify({
            "error": "Product not found on Open Food Facts"
        }), 404

    product = products[0]

    result = {
        "product_name": product.get(
            "product_name",
            ""
        ),
        "brand": product.get(
            "brands",
            ""
        ),
        "ingredients": product.get(
            "ingredients_text",
            ""
        ),
        "categories": product.get(
            "categories",
            ""
        ),
        "image_url": product.get(
            "image_url",
            ""
        )
    }

    return jsonify(result), 200


# ADD PRODUCT FROM OPEN FOOD FACTS
@app.route(
    "/inventory/from-api/<path:product_name>",
    methods=["POST"]
)
def add_product_from_api(product_name):

    data = fetch_product_from_openfoodfacts(product_name)

    if data is None:
        return jsonify({
            "error": "Open Food Facts is currently unavailable"
        }), 503

    products = data.get("products", [])

    if not products:
        return jsonify({
            "error": "Product not found on Open Food Facts"
        }), 404

    product = products[0]

    new_id = max(
        [item["id"] for item in inventory],
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "product_name": product.get(
            "product_name",
            "Unknown product"
        ),
        "brand": product.get(
            "brands",
            ""
        ),
        "ingredients": product.get(
            "ingredients_text",
            ""
        ),
        "price": 0,
        "stock": 0
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


# HOME ROUTE
@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Inventory Management API is running",
        "endpoints": {
            "GET all inventory": "/inventory",
            "GET one item": "/inventory/<id>",
            "POST new item": "/inventory",
            "PATCH item": "/inventory/<id>",
            "DELETE item": "/inventory/<id>",
            "GET product from API": "/api/product/<product_name>",
            "POST product from API": "/inventory/from-api/<product_name>"
        }
    }), 200


# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True)