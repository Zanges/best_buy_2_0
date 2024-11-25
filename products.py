import sys

from promotion import Promotion


class Product:
    def __init__(self, name: str, price: float, quantity: int) -> None:
        """
        Constructor for the Product class
        :param name: str: Name of the product
        :param price: float: Price of the product
        :param quantity: int: Quantity of the product
        """
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non empty string")
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer")
        if price < 0:
            raise ValueError("Price must be non-negative")
        if quantity < 0:
            raise ValueError("Quantity must be non-negative")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = False if quantity == 0 else True
        self.promotion = None

    def get_quantity(self) -> float: # Not sure why the documentation says it should return float. I think quantity should be an integer
        """ Returns the quantity of the product """
        return float(self.quantity)

    def set_quantity(self, quantity: int) -> None:
        """ Sets the quantity of the product and deactivates it if quantity is 0 """
        if not isinstance(quantity, int):
            raise ValueError("New quantity must be an integer")
        if quantity < 0:
            raise ValueError("New quantity must be non-negative")
        if quantity == 0:
            self.active = False
        self.quantity = quantity

    def is_active(self) -> bool:
        """ Returns whether the product is active or not """
        return self.active

    def activate(self) -> None:
        """ Activates the product """
        self.active = True

    def deactivate(self) -> None:
        """ Deactivates the product """
        self.active = False

    def __str__(self) -> str:
        """ Returns the string representation of the product """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Promotion: {self.promotion}"

    def show(self) -> str:
        """
        Alias for __str__
        Returns the string representation of the product
        """
        return self.__str__()

    def buy(self, quantity: int) -> float:
        """
        Buys the product and returns the total cost
        :param quantity: int: Quantity of the product to buy
        :return: float: Total cost of the product
        """
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer")
        if quantity < 0:
            raise ValueError("Quantity must be non-negative")
        if quantity > self.quantity:
            raise ValueError("Not enough quantity in stock")
        self.set_quantity(self.quantity - quantity)
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def set_promotion(self, promotion: Promotion) -> None:
        """ Sets the promotion for the product """
        self.promotion = promotion

    def get_promotion(self) -> Promotion or None:
        """ Returns the promotion for the product """
        return self.promotion


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float) -> None:
        """
        Constructor for the NonStockedProduct class

        :param name:
        :param price:
        """
        super().__init__(name, price, sys.maxsize) # not sure if sys.maxsize is the best way to represent infinity
        self.active = True

    def set_quantity(self, quantity: int) -> None:
        """ Raises an error as quantity cannot be set for non stocked product """
        raise ValueError("Cannot set quantity for non stocked product")

    def buy(self, quantity: int) -> float:
        """
        Buys the product and returns the total cost
        :param quantity: int: Quantity of the product to buy
        :return: float: Total cost of the product
        """
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer")
        if quantity < 0:
            raise ValueError("Quantity must be non-negative")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def __str__(self) -> str:
        """ Returns the string representation of the product """
        super_str = super().__str__()
        super_str = super_str.replace(f"Quantity: {sys.maxsize}", "Quantity: ∞")
        return super_str


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, limit: int) -> None:
        """
        Constructor for the LimitedProduct class

        :param name:
        :param price:
        :param quantity:
        :param limit:
        """
        if not isinstance(limit, int):
            raise ValueError("Limit must be an integer")
        if limit < 0:
            raise ValueError("Limit must be non-negative")
        super().__init__(name, price, quantity)
        self.limit = limit

    def buy(self, quantity: int) -> float:
        """
        Buys the product and returns the total cost
        :param quantity: int: Quantity of the product to buy
        :return: float: Total cost of the product
        """
        if quantity > self.limit:
            raise ValueError(f"Quantity must be less than or equal to {self.limit}")
        return super().buy(quantity)

    def __str__(self) -> str:
        """ Returns the string representation of the product """
        return f"{super().__str__()}, Limit: {self.limit}"

    def set_limit(self, limit: int) -> None:
        """ Sets the limit of the product """
        if not isinstance(limit, int):
            raise ValueError("Limit must be an integer")
        if limit <= 0:
            raise ValueError("Limit must be non-negative")
        self.limit = limit

    def get_limit(self) -> int:
        """ Returns the limit of the product """
        return self.limit


def main():
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show() # As specified in the documentation, this returns a string and doesn't print anything by itself.
    print(bose.show()) # This prints the string representation of the product
    mac.show()
    print(mac) # This also prints the string representation of the product

    bose.set_quantity(1000)
    bose.show()
    print(bose)


if __name__ == "__main__":
    main()