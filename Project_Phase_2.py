## *************************************************************** ##
## MSCS 532 - Algorithms and Data Structures
## Project Phase 2
## Inventory Management System
## Shrisan kapali - 005032249
## *************************************************************** ##

## Dyanamic Inventory Management System
## This program will allow end users to perform CRUD operations on products and categories
from datetime import datetime
import time


# Defining the class Category
# A category has unique id assigned to it
# A category has a name and the status can be active or inactive i.e, true or false
class Category:
    # Constructor to initialize a category class object
    def __init__(self, cagetory_id: int, name: str, status: bool = True):
        self.category_id = cagetory_id
        self.name = name
        self.status = status

    # Perform update on a category
    # Only perform update on the passed in value
    def update(self, name: str = None, status: bool = None):
        if name:
            self.name = name
        if status is not None:
            self.status = status

    # Printing the category when print command is used
    # Print layout Example "Category 1, Name Grocery, Current Status Active"
    def __repr__(self):
        return f"Category ({self.category_id}), Name {self.name}, Current Status {'Active' if self.status else 'Inactive'}"


# Defining class Product
# A product has id, name, description, quantity and belongs to the category
class Product:
    # Constructor to initialize the product class
    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
        description: str,
        category: Category,
        quantity: int,
    ):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.quantity = quantity
        self.price_history = [(datetime.now(), price)]  # a list of price history

    # A function to update product information
    def update(
        self,
        name: str = None,
        price: float = None,
        description: str = None,
        category: Category = None,
        quantity: int = None,
    ):
        if name:
            self.name = name
        # Only if the passed in price is not equal to old price
        if price is not None and price != self.price:
            self.price = price
            # Append the new price in the price history list
            self.price_history.append((datetime.now(), price))
        if description:
            self.description = description
        if category:
            self.category = category
        if quantity is not None and quantity != self.quantity:
            self.quantity = quantity

    # A function to increase quantity
    def increaseQuantity(self, increaseBy: int):
        self.quantity += increaseBy

    # A function to decrease quantity
    def decreaseQuantity(self, increaseBy: int):
        self.quantity -= increaseBy

    # A function to print the product class
    def __repr__(self):
        return f"Product Id: {self.product_id}, Product Price: {self.price}, Product Name: {self.name}, Description: {self.description}, Quantity: {self.quantity}, Category:{self.category.name}"


# Finally as we now have product and category class, create Inventory class
class Inventory:

    # Intialize inventory class with empty categories and product dictionary
    def __init__(self):
        self.categories = {}
        self.products = {}

    ## ******************************************** ##
    # Inventory Category Management
    ## ******************************************** ##
    # Functions to add and update category and products
    # Each id needs to be unique so
    def is_category_id_unique(self, category_id: int) -> bool:
        return category_id not in self.categories

    # Also check if product id is unique
    def is_product_id_unique(self, product_id: int) -> bool:
        return product_id not in self.products

    # Add new category
    def add_new_category(self, category_id: int, name: str, status: bool = True):
        # First check if the category id is unique
        if not self.is_category_id_unique(category_id):
            raise ValueError("Category Id must be unique. This id already exists")

        # Add the category using category_id as key
        self.categories[category_id] = Category(category_id, name, status)

    # Update Category name or status
    def update_category(self, cagetory_id: int, name: str = None, status: bool = None):
        # If passed in category id is not present, return error
        if cagetory_id not in self.categories:
            raise ValueError(
                "Unable to find the category for this passed in cateogry id"
            )

        # Use category update method to update the category details
        self.categories[cagetory_id].update(name, status)

    # Delete existing category
    def delete_category(self, cagetory_id: int):
        # If passed in category id is not present, return error
        if cagetory_id not in self.categories:
            raise ValueError(
                "Unable to find the category for this passed in cateogry id"
            )

        del self.categories[cagetory_id]

    # A function to search category by name
    def search_category_by_name(self, name: str):
        return [
            category
            for category in self.categories.values()
            if name.lower() in category.name.lower()
        ]

    ## ******************************************** ##
    # Inventory Product Management
    ## ******************************************** ##

    # Add in a new product
    def add_product(
        self,
        product_id: int,
        name: str,
        price: float,
        description: str,
        category_id: int,
        quantity: int,
    ):
        # First check if the product id is unique
        if not self.is_product_id_unique(product_id):
            raise ValueError("Product with the same id already exists.")

        # Now check if the category id exists
        if category_id not in self.categories:
            raise ValueError("Passed in category id is invalid")

        # Extract the category
        category = self.categories[category_id]

        # Finally add in the product
        self.products[product_id] = Product(
            product_id, name, price, description, category, quantity
        )

    # Update the existing product details
    def update_product(
        self,
        product_id: int,
        name: str = None,
        price: float = None,
        description: str = None,
        category_id: int = None,
        quantity: int = None,
    ):
        if product_id not in self.products:
            raise ValueError("Unable to find product using the passed in id")

        # Get existing product
        product = self.products[product_id]

        # Check if category changed, if changed get the new category
        # If new category id exists, get the category by id or use existing
        category = (
            self.categories.get(category_id, product.category)
            if category_id
            else product.category
        )

        # Finally call in product update function to update the values
        product.update(name, price, description, category, quantity)

    # Increase product quantity by quantity
    def increase_product_quantity(self, product_id: int, quantity: int):
        if product_id not in self.products:
            raise ValueError("Unable to find the product using passed in id")

        self.products[product_id].increaseQuantity(quantity)

    # Decrease product quantity by quantity
    def decrease_product_quantity(self, product_id: int, quantity: int):
        if product_id not in self.products:
            raise ValueError("Unable to find the product using passed in id")

        self.products[product_id].decreaseQuantity(quantity)

    # View product price history
    def get_product_price_history(self, product_id: int):
        if product_id not in self.products:
            raise ValueError("Unable to find the product using passed in id")

        return self.products[product_id].price_history

    # Search product by name
    def search_product_by_name(self, name: str):
        return [
            product
            for product in self.products.values()
            if name.lower() in product.name.lower()
        ]

    # Search product by price range
    def search_product_by_price_range(self, min_price: float, max_price: float):
        return [
            product
            for product in self.products.values()
            if min_price <= product.price <= max_price
        ]

    # Search product by category id
    def search_product_by_category_id(self, category_id: int):
        return [
            product
            for product in self.products.values()
            if product.category.category_id == category_id
        ]

    # Search product by category name
    def search_product_by_category_name(self, name: str):
        return [
            product
            for product in self.products.values()
            if name.lower() in product.category.name.lower()
        ]

    # Finally a product to print the inventory class
    def __repr__(self):
        return f"Inventory Details \nCategories:{list(self.categories.values())}, \n\nProducts:{list(self.products.values())})"


## ************************************* ##
## Test Cases
## ************************************* ##

# Building the inventory class
inventory = Inventory()
print("##########################################")
print("Initializing the Grocery Store Inventory")
print("##########################################")

# Loading categories to the inventory
print("")
print("##########################################")
print("Loading categories to the inventory ...")
# Creating a list of categories to be loaded
categoriesList = [
    {"id": 1, "name": "Vegetables", "status": True},
    {"id": 2, "name": "Diary", "status": True},
    {"id": 3, "name": "Meat", "status": True},
    {"id": 4, "name": "Bakery", "status": True},
    {"id": 5, "name": "Liquor", "status": True},
    {"id": 6, "name": "Drinks", "status": True},
    {"id": 7, "name": "Cleaning", "status": True},
    {"id": 8, "name": "Health", "status": True},
    {"id": 9, "name": "House", "status": True},
]
# A variable to store category addition execution times
loadingCategoryExecutionTimes = []

print("Loading categories ")
for category in categoriesList:
    # Calculating the execution time to load
    start_time = time.time()
    inventory.add_new_category(category["id"], category["name"], category["status"])
    end_time = time.time()
    exec_time = end_time - start_time
    # Add this execution times to a list
    loadingCategoryExecutionTimes.append(
        {"categoryId": category["id"], "execution_time": exec_time}
    )
    print(
        f"Category with Id: {category['id']}, Name: {category['name']}, Status: {category['status']} loaded in {exec_time} seconds"
    )

print("##########################################")
print("")
print("##########################################")
print("Loading products to the inventory")

productsList = [
    # Products for category vegetables (1)
    {
        "id": 1,
        "name": "Mustard Greens Spinach",
        "price": 1.49,
        "description": "Spinach",
        "category": 1,
        "quantity": 100,
    },
    {
        "id": 2,
        "name": "Caluliflower",
        "price": 3.50,
        "description": "Per piece",
        "category": 1,
        "quantity": 50,
    },
    {
        "id": 3,
        "name": "Potato",
        "price": 5.50,
        "description": "5 lb bag",
        "category": 1,
        "quantity": 80,
    },
    {
        "id": 4,
        "name": "Coriander",
        "price": 0.50,
        "description": "Per piece",
        "category": 1,
        "quantity": 200,
    },
    # Products for category Diary (2)
    {
        "id": 5,
        "name": "Whole Milk",
        "price": 3.99,
        "description": "Per piece",
        "category": 2,
        "quantity": 20,
    },
    {
        "id": 6,
        "name": "Eggnog",
        "price": 4.99,
        "description": "Per piece",
        "category": 2,
        "quantity": 10,
    },
    {
        "id": 7,
        "name": "Greek Yogurt",
        "price": 5.99,
        "description": "Per piece",
        "category": 2,
        "quantity": 30,
    },
    # Products for category Meat (3)
    {
        "id": 8,
        "name": "Chicken Breast",
        "price": 15.99,
        "description": "3.99 per lbs",
        "category": 3,
        "quantity": 8,
    },
    {
        "id": 9,
        "name": "Chicken Leg Quarter",
        "price": 6.99,
        "description": "1.99 per lbs",
        "category": 3,
        "quantity": 12,
    },
    {
        "id": 10,
        "name": "Chicken Thigh",
        "price": 10.99,
        "description": "2.99 per lbs",
        "category": 3,
        "quantity": 15,
    },
    # Products for category Bakery (4)
    {
        "id": 11,
        "name": "White Bread",
        "price": 3.99,
        "description": "Per piece",
        "category": 4,
        "quantity": 15,
    },
    {
        "id": 12,
        "name": "Bagel",
        "price": 5.99,
        "description": "Per Packet 4 pcs",
        "category": 4,
        "quantity": 7,
    },
    # Products for category Liquor (5)
    {
        "id": 13,
        "name": "Corona Beer",
        "price": 10.99,
        "description": "4 cans",
        "category": 5,
        "quantity": 10,
    },
    {
        "id": 14,
        "name": "Hennessy",
        "price": 80.99,
        "description": "750 ml",
        "category": 5,
        "quantity": 10,
    },
    # Products for category Drinks (6)
    {
        "id": 15,
        "name": "Coke",
        "price": 1.99,
        "description": "1 L",
        "category": 6,
        "quantity": 10,
    },
    {
        "id": 16,
        "name": "Fanta",
        "price": 1.99,
        "description": "1 L",
        "category": 6,
        "quantity": 13,
    },
    {
        "id": 17,
        "name": "Diet Coke",
        "price": 2.50,
        "description": "1 L",
        "category": 6,
        "quantity": 20,
    },
    {
        "id": 18,
        "name": "Diet Fanta",
        "price": 3.50,
        "description": "1 L",
        "category": 6,
        "quantity": 25,
    },
    # Products for category Cleaning (7)
    {
        "id": 19,
        "name": "Dish Wash Liquid",
        "price": 3.50,
        "description": "500 ml",
        "category": 7,
        "quantity": 10,
    },
    {
        "id": 20,
        "name": "Dish Wash Scrub",
        "price": 1.50,
        "description": "Per piece",
        "category": 7,
        "quantity": 40,
    },
    # Products for category Health (8)
    {
        "id": 21,
        "name": "Toothpaste",
        "price": 2.50,
        "description": "Per piece",
        "category": 8,
        "quantity": 20,
    },
    {
        "id": 22,
        "name": "Toothbrush",
        "price": 4.50,
        "description": "Per piece",
        "category": 8,
        "quantity": 25,
    },
    # Products for category House (9)
    {
        "id": 23,
        "name": "Carpet Cleaner",
        "price": 5.50,
        "description": "Per piece",
        "category": 9,
        "quantity": 5,
    },
    {
        "id": 24,
        "name": "Mop",
        "price": 14.50,
        "description": "Per piece",
        "category": 9,
        "quantity": 2,
    },
]

# A variable to store product addition execution times
loadingProductsExecutionTimes = []
for product in productsList:
    # Calculating the execution time to load
    start_time = time.time()
    inventory.add_product(
        product["id"],
        product["name"],
        product["price"],
        product["description"],
        product["category"],
        product["quantity"],
    )
    end_time = time.time()
    exec_time = end_time - start_time
    # Add this execution times to a list
    loadingProductsExecutionTimes.append(
        {"product_id": product["id"], "execution_time": exec_time}
    )
    print(
        f"Product with Id: {product['id']}, Name: {product['name']} loaded in {exec_time} seconds"
    )
print("##########################################")

print("")
print("##########################################")
print("Current inventory status")
print(inventory)


print("")
print("##########################################")
print("Testing the functions")

print("")
print("##########################################")
print("Test for class Category")
print("##########################################")
print("Updating category 1 name from Vegetables to Produce")
print("Before Update: ", inventory.categories[1])
start_time = time.time()
inventory.update_category(1, "Produce")
end_time = time.time()
exec_time = end_time - start_time
print("After Update: ", inventory.categories[1])
print(f"Update took about {exec_time} seconds")

print("")
print("Adding a new category with id 10")
inventory.add_new_category(10, "Electronics", True)
print("\nUpdated categories list")
for i in range(len(inventory.categories)):
    print(inventory.categories[i + 1])

print("\nFind the category by name - produce")
start_time = time.time()
categories = inventory.search_category_by_name("Produce")
end_time = time.time()
exec_time = end_time - start_time
print(f"Categories found {list(categories)} in {exec_time} seconds")

print("\nDeleting category - electornic")
print(
    f"Before delete using search to find electronics - {inventory.search_category_by_name("Electronics")}"
)
start_time = time.time()
inventory.delete_category(10)
end_time = time.time()
print(
    f"After delete using search to find electronics - {inventory.search_category_by_name("Electronics")}"
)
print("##########################################")

print("\n\n##########################################")
print("Test for class Products")
print("##########################################")

print("Updating product 1 price from 1.49 to 1.99")
print("Before Update: ", inventory.products[1])
start_time = time.time()
inventory.update_product(1, None, 1.99, None, None, None)
end_time = time.time()
exec_time = end_time - start_time
print("After Update: ", inventory.products[1])
print(f"Update took about {exec_time} seconds")

print("\nIncrease the quanity of product id 1 by 25")
start_time = time.time()
inventory.increase_product_quantity(1, 25)
end_time = time.time()
exec_time = end_time - start_time
print("After Update: ", inventory.products[1])
print(f"Update took about {exec_time} seconds")

print("\nDecrease the quanity of product id 1 by 5")
start_time = time.time()
inventory.decrease_product_quantity(1, 5)
end_time = time.time()
exec_time = end_time - start_time
print("After Update: ", inventory.products[1])
print(f"Update took about {exec_time} seconds")

print("\nGet product price history")
start_time = time.time()
priceHistory = inventory.get_product_price_history(1)
end_time = time.time()
exec_time = end_time - start_time
print("Price History of product 1: ", priceHistory)
print(f"Extraction took about {exec_time} seconds")

print("\nSearch product by name")
start_time = time.time()
products = inventory.search_product_by_name("mustard greens")
end_time = time.time()
exec_time = end_time - start_time
print("Searching for product with name mustard greens: ", products)
print(f"Extraction took about {exec_time} seconds")

print("\nSearch product by price range")
start_time = time.time()
products = inventory.search_product_by_price_range(5.99, 10.99)
end_time = time.time()
exec_time = end_time - start_time
print("Searching for product with within price range 5.99-10.99: ", products)
print(f"Extraction took about {exec_time} seconds")

print("\nSearch product by category id")
start_time = time.time()
products = inventory.search_product_by_category_id(1)
end_time = time.time()
exec_time = end_time - start_time
print("Searching for product with category 1 ", products)
print(f"Extraction took about {exec_time} seconds")

print("\nSearch product by category name produce")
start_time = time.time()
products = inventory.search_product_by_category_name("produce")
end_time = time.time()
exec_time = end_time - start_time
print("Searching for product with category 1 ", products)
print(f"Extraction took about {exec_time} seconds")
print("##########################################")
