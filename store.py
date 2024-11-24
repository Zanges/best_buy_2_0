from typing import List

from products import Product


class Store:

    def __init__(self, products: List[Product]) -> None:
        """
        Constructor for the Store class
        :param products: List[Product]: List of products in the store
        """
        if not all(isinstance(product, Product) for product in products):
            raise ValueError("All elements of products must be of type Product")

        self.products = products

    def add_product(self, product: Product) -> None:
        """ Adds a product to the store """
        if not isinstance(product, Product):
            raise ValueError("Product must be of type Product")
        if product in self.products:
            raise ValueError("Product already exists in the store")

        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        """ Removes a product from the store """
        if not isinstance(product, Product):
            raise ValueError("Product must be of type Product")
        if product not in self.products:
            raise ValueError("Product does not exist in the store")

        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """ Returns the total quantity of all products in the store """
        return sum(product.quantity for product in self.products)

    def get_all_products(self) -> List[Product]:
        """ Returns all active products in the store """
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        """
        Orders products from the store
        :param shopping_list: list[tuple[Product, int]]: List of tuples where the first element is the product and the second element is the quantity
        :return: float: Total cost of the order
        """
        total_cost = 0
        for product, quantity in shopping_list:
            if product not in self.products:
                raise ValueError("Product does not exist in the store")
            shop_product = self.products[self.products.index(product)] # just to ensure that the product is the same object in the store
            if not shop_product.is_active():
                raise ValueError("Product is not active")

            try:
                total_cost += shop_product.buy(quantity)
            except ValueError as e:
                print(f"Error buying {shop_product}: {e}")

        return total_cost


def main():
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    ]

    store = Store(product_list)
    products = store.get_all_products()
    print(store.get_total_quantity())
    print(store.order([(products[0], 1), (products[1], 2)]))


if __name__ == "__main__":
    main()