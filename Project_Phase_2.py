## *************************************************************** ##
## MSCS 532 - Algorithms and Data Structures
## Project Phase 2
## Inventory Management System
## Shrisan kapali - 005032249
## *************************************************************** ##

## Dyanamic Inventory Management System
## This program will allow end users to perform CRUD operations on products and categories
from datetime import datetime


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
            self.price_history.append(datetime.now(), price)
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
        return f"Product Id: {self.product_id}, Product Name: {self.name}, Description: {self.description}, Quantity: {self.quantity}, Category:{self.category.name}"


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
        if product_id in self.products:
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
            if product.category.id == category_id
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
        return f"Inventory(Categories:{list(self.categories.values())}, Products:{list:(self.products.values())})"
