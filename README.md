# Inventory Management System
This is a simple inventory management system built with Python and Flask.

The purpose of this project is to create a REST API that allows users to add, view, update, and delete inventory items. It also connects to the Open Food Facts API to get additional information about food products.

## What This Project Does
The system can:

- View all inventory items

- View one inventory item

- Add a new inventory item

- Update an inventory item

- Delete an inventory item

- Find products using the Open Food Facts API

- Add products from Open Food Facts to the inventory

- Use a command-line interface (CLI)

- Run tests to check that the API works correctly

## Installation
First, create a virtual environment:
- python3 -m venv .venv

Activate the virtual environment:
- source .venv/bin/activate

Install the required packages:
- pip install -r requirements.txt


## Running the Application
Start the Flask application with:
- python3 app.py

The application should run at:
http://127.0.0.1:5000



# Open Food Facts API
The project connects to the Open Food Facts API to get additional product information.

## The API can provide information such as:

- Product name

- Brand

- Ingredients

- Categories

- Product image



# CLI
The project has a command-line interface that allows users to interact with the Flask API.

First, start the Flask application:
- python3 app.py

Then open another terminal, activate the virtual environment, and run:
- python3 cli.py

## The CLI provides options for:

1. Viewing inventory

2. Viewing one item

3. Adding an item

4. Updating an item

5. Deleting an item

6. Finding a product using Open Food Facts

7. Adding a product from Open Food Facts

## Testing
The project uses pytest for testing.

## If pytest is not installed, run:
- pip install pytest

To run the tests:
- pytest