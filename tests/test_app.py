import sys
sys.path.append(".")

from app import app
from unittest.mock import patch


# Test GET all inventory
def test_get_inventory():
    client = app.test_client()

    response = client.get("/inventory")

    assert response.status_code == 200


# Test GET one inventory item
def test_get_item():
    client = app.test_client()

    response = client.get("/inventory/1")

    assert response.status_code == 200


# Test GET item that does not exist
def test_get_item_not_found():
    client = app.test_client()

    response = client.get("/inventory/999")

    assert response.status_code == 404


# Test POST new inventory item
def test_create_item():
    client = app.test_client()

    data = {
        "product_name": "Apple Juice",
        "brand": "Tropicana",
        "ingredients": "Apples, water",
        "price": 4.99,
        "stock": 10
    }

    response = client.post(
        "/inventory",
        json=data
    )

    assert response.status_code == 201


# Test PATCH inventory item
def test_update_item():
    client = app.test_client()

    data = {
        "price": 6.99,
        "stock": 25
    }

    response = client.patch(
        "/inventory/1",
        json=data
    )

    assert response.status_code == 200


# Test DELETE inventory item
def test_delete_item():
    client = app.test_client()

    response = client.delete("/inventory/1")

    assert response.status_code == 200


# Test Open Food Facts API
@patch("app.requests.get")
def test_openfoodfacts(mock_get):
    client = app.test_client()

    # Fake Open Food Facts response
    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = {
        "products": [
            {
                "product_name": "Organic Almond Milk",
                "brands": "Silk",
                "ingredients_text": "Filtered water, almonds"
            }
        ]
    }

    response = client.get(
        "/api/product/Organic%20Almond%20Milk"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["product_name"] == "Organic Almond Milk"
    assert data["brand"] == "Silk"
