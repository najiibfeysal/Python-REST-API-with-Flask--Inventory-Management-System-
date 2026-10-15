
import cli
from unittest.mock import patch, Mock


# Test viewing all inventory
@patch("cli.requests.get")
def test_view_inventory(mock_get, capsys):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brand": "Silk",
            "ingredients": "Water, almonds",
            "price": 5.99,
            "stock": 20
        }
    ]

    cli.view_inventory()

    output = capsys.readouterr().out

    assert "Organic Almond Milk" in output
    assert "Silk" in output
    assert "5.99" in output


# Test viewing one inventory item
@patch("cli.requests.get")
def test_view_item(mock_get, capsys):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "id": 1,
        "product_name": "Nutella",
        "brand": "Ferrero",
        "ingredients": "Sugar, cocoa",
        "price": 7.99,
        "stock": 15
    }

    with patch("builtins.input", return_value="1"):
        cli.view_item()

    output = capsys.readouterr().out

    assert "Nutella" in output
    assert "Ferrero" in output


# Test adding a new inventory item
@patch("cli.requests.post")
def test_add_item(mock_post, capsys):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "id": 3,
        "product_name": "Apple Juice",
        "brand": "Tropicana",
        "ingredients": "Apples, water",
        "price": 4.99,
        "stock": 10
    }

    inputs = [
        "Apple Juice",
        "Tropicana",
        "Apples, water",
        "4.99",
        "10"
    ]

    with patch("builtins.input", side_effect=inputs):
        cli.add_item()

    output = capsys.readouterr().out

    assert "Item added successfully!" in output
    mock_post.assert_called_once()


# Test updating inventory stock
@patch("cli.requests.patch")
def test_update_item(mock_patch, capsys):
    mock_patch.return_value.status_code = 200
    mock_patch.return_value.json.return_value = {
        "id": 1,
        "product_name": "Nutella",
        "brand": "Ferrero",
        "ingredients": "Sugar, cocoa",
        "price": 7.99,
        "stock": 30
    }

    inputs = ["1", "5", "30"]

    with patch("builtins.input", side_effect=inputs):
        cli.update_item()

    output = capsys.readouterr().out

    assert "Item updated successfully!" in output
    mock_patch.assert_called_once()


# Test deleting an inventory item
@patch("cli.requests.delete")
def test_delete_item(mock_delete, capsys):
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {
        "message": "Inventory item deleted successfully"
    }

    with patch("builtins.input", return_value="1"):
        cli.delete_item()

    output = capsys.readouterr().out

    assert "Inventory item deleted successfully" in output
    mock_delete.assert_called_once()


# Test searching for an external product
@patch("cli.requests.get")
def test_find_product(mock_get, capsys):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "product_name": "Nutella",
        "brand": "Ferrero",
        "ingredients": "Sugar, palm oil, hazelnuts",
        "categories": "Spreads",
        "image_url": "https://example.com/nutella.jpg"
    }

    with patch("builtins.input", return_value="Nutella"):
        cli.find_product()

    output = capsys.readouterr().out

    assert "Product found!" in output
    assert "Nutella" in output
    assert "Ferrero" in output


# Test importing a product from the external API
@patch("cli.requests.post")
def test_add_product_from_api(mock_post, capsys):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "id": 3,
        "product_name": "Nutella",
        "brand": "Ferrero",
        "ingredients": "Sugar, cocoa",
        "price": 0,
        "stock": 0
    }

    with patch("builtins.input", return_value="Nutella"):
        cli.add_product_from_api()

    output = capsys.readouterr().out

    assert "Product added from Open Food Facts!" in output
    mock_post.assert_called_once()


# Test invalid item ID
@patch("builtins.input", return_value="abc")
def test_view_item_invalid_id(mock_input, capsys):
    cli.view_item()

    output = capsys.readouterr().out

    assert "ID must be a number." in output


# Test exiting the main menu
@patch("builtins.input", side_effect=["8"])
def test_main_exit(mock_input, capsys):
    cli.main()

    output = capsys.readouterr().out

    assert "Goodbye!" in output
