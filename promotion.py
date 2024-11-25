from abc import ABC, abstractmethod


class Promotion(ABC):
    @abstractmethod
    def __init__(self, name: str):
        """ Initializes the promotion with a name """
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name) == 0:
            raise ValueError("Name must not be empty")

        self.name = name

    def __str__(self):
        """ Returns the name of the promotion """
        return self.name

    @abstractmethod
    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """ Applies the promotion to the product and returns the total cost """
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer")
        if quantity < 0:
            raise ValueError("Quantity must be non-negative")


class SecondHalfPricePromotion(Promotion):
    def __init__(self):
        """ Initializes the second half price promotion with a name, so str() can return a human-readable name """
        super().__init__("Second Half Price!")

    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """ Applies the second half price promotion to the product and returns the total cost """
        super().apply_promotion(product, quantity)
        if quantity == 0:
            return 0

        total_cost = 0
        for i in range(1, quantity + 1):
            if i % 2 == 0:
                total_cost += product.price / 2
            else:
                total_cost += product.price

        return total_cost


class ThirdOneFreePromotion(Promotion):
    def __init__(self):
        """ Initializes the third one free promotion with a name, so str() can return a human-readable name """
        super().__init__("Third One Free!")

    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """ Applies the third one free promotion to the product and returns the total cost """
        super().apply_promotion(product, quantity)
        if quantity == 0:
            return 0

        total_cost = 0
        for i in range(1, quantity + 1):
            if i % 3 == 0:
                continue
            total_cost += product.price

        return total_cost


class PercentDiscountPromotion(Promotion):
    def __init__(self, percent: float):
        """ Initializes the percent discount promotion with a name and a percent discount """
        if not isinstance(percent, (int, float)):
            raise ValueError("Discount must be a float")
        if percent < 0:
            raise ValueError("Discount must be non-negative")
        super().__init__(f"{percent}% Discount!")
        self.percent = percent

    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """ Applies the percent discount promotion to the product and returns the total cost """
        super().apply_promotion(product, quantity)
        if quantity == 0:
            return 0

        return product.price * quantity * (1 - self.percent / 100)


def main():
    pass


if __name__ == "__main__":
    main()