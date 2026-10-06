import requests


BASE_URL = "http://127.0.0.1:5000"


# GET ALL INVENTORY
def view_inventory():

    response = requests.get(
        f"{BASE_URL}/inventory"
    )

    if response.status_code == 200:

        items = response.json()

        if not items:
            print("Inventory is empty.")
            return

        for item in items:

            print("\nID:", item["id"])
            print("Product:", item["product_name"])
            print("Brand:", item["brand"])
            print("Ingredients:", item["ingredients"])
            print("Price:", item["price"])
            print("Stock:", item["stock"])

    else:

        print("Error:", response.json())


# GET ONE ITEM
def view_item():

    item_id = input("Enter item ID: ")

    try:
        item_id = int(item_id)

    except ValueError:
        print("ID must be a number.")
        return

    response = requests.get(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:

        item = response.json()

        print("\nID:", item["id"])
        print("Product:", item["product_name"])
        print("Brand:", item["brand"])
        print("Ingredients:", item["ingredients"])
        print("Price:", item["price"])
        print("Stock:", item["stock"])

    else:

        print(
            "Error:",
            response.json().get("error")
        )


# ADD NEW ITEM
def add_item():

    product_name = input("Product name: ")
    brand = input("Brand: ")
    ingredients = input("Ingredients: ")

    try:

        price = float(
            input("Price: ")
        )

        stock = int(
            input("Stock: ")
        )

    except ValueError:

        print(
            "Price must be a number and stock "
            "must be an integer."
        )

        return

    data = {
        "product_name": product_name,
        "brand": brand,
        "ingredients": ingredients,
        "price": price,
        "stock": stock
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )

    if response.status_code == 201:

        print("\nItem added successfully!")
        print(response.json())

    else:

        print("Error:", response.json())


# UPDATE ITEM
def update_item():

    item_id = input("Enter item ID: ")

    try:

        item_id = int(item_id)

    except ValueError:

        print("ID must be a number.")
        return

    print("\nWhat do you want to update?")
    print("1. Product name")
    print("2. Brand")
    print("3. Ingredients")
    print("4. Price")
    print("5. Stock")

    choice = input("Choose an option: ")

    data = {}

    if choice == "1":

        data["product_name"] = input(
            "New product name: "
        )

    elif choice == "2":

        data["brand"] = input(
            "New brand: "
        )

    elif choice == "3":

        data["ingredients"] = input(
            "New ingredients: "
        )

    elif choice == "4":

        try:

            data["price"] = float(
                input("New price: ")
            )

        except ValueError:

            print("Price must be a number.")
            return

    elif choice == "5":

        try:

            data["stock"] = int(
                input("New stock: ")
            )

        except ValueError:

            print("Stock must be an integer.")
            return

    else:

        print("Invalid option.")
        return

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    if response.status_code == 200:

        print("\nItem updated successfully!")
        print(response.json())

    else:

        print("Error:", response.json())


# DELETE ITEM
def delete_item():

    item_id = input("Enter item ID: ")

    try:

        item_id = int(item_id)

    except ValueError:

        print("ID must be a number.")
        return

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:

        print(
            response.json()["message"]
        )

    else:

        print(
            "Error:",
            response.json().get("error")
        )


# FIND PRODUCT ON OPEN FOOD FACTS
def find_product():

    product_name = input(
        "Enter product name: "
    )

    response = requests.get(
        f"{BASE_URL}/api/product/{product_name}"
    )

    if response.status_code == 200:

        product = response.json()

        print("\nProduct found!")

        print(
            "Product:",
            product["product_name"]
        )

        print(
            "Brand:",
            product["brand"]
        )

        print(
            "Ingredients:",
            product["ingredients"]
        )

        print(
            "Categories:",
            product["categories"]
        )

        if product["image_url"]:

            print(
                "Image:",
                product["image_url"]
            )

    else:

        error = response.json().get(
            "error",
            "Unknown error"
        )

        print(
            "Error:",
            error
        )


# ADD PRODUCT FROM OPEN FOOD FACTS
def add_product_from_api():

    product_name = input(
        "Enter product name: "
    )

    response = requests.post(
        f"{BASE_URL}/inventory/from-api/{product_name}"
    )

    if response.status_code == 201:

        print(
            "\nProduct added from Open Food Facts!"
        )

        print(
            response.json()
        )

    else:

        print(
            "Error:",
            response.json()
        )


# MAIN MENU
def main():

    while True:

        print(
            "\n- INVENTORY MANAGEMENT SYSTEM -"
        )

        print("1. View all inventory")
        print("2. View one item")
        print("3. Add inventory item")
        print("4. Update inventory item")
        print("5. Delete inventory item")
        print("6. Find product on Open Food Facts")
        print("7. Add product from Open Food Facts")
        print("8. Exit")

        choice = input(
            "\nChoose an option: "
        )

        if choice == "1":

            view_inventory()

        elif choice == "2":

            view_item()

        elif choice == "3":

            add_item()

        elif choice == "4":

            update_item()

        elif choice == "5":

            delete_item()

        elif choice == "6":

            find_product()

        elif choice == "7":

            add_product_from_api()

        elif choice == "8":

            print("Goodbye!")
            break

        else:

            print(
                "Invalid option. Please choose 1-8."
            )


if __name__ == "__main__":
    main()