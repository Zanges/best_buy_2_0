import pytest

from promotion import *


class TestSecondHalfPricePromotion:
    def test_apply_promotion(self):
        product = Product("Test Product", 100, 100)
        promotion = SecondHalfPricePromotion()
        assert promotion.apply_promotion(product, 10) == 750

    def test_apply_promotion_with_invalid_product(self):
        promotion = SecondHalfPricePromotion()
        with pytest.raises(ValueError) as e:
            promotion.apply_promotion("Test Product", 10)
        assert str(e.value) == "Product must be of type Product"

    def test_apply_promotion_with_invalid_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = SecondHalfPricePromotion()
        with pytest.raises(ValueError) as e:
            promotion.apply_promotion(product, "10")
        assert str(e.value) == "Quantity must be an integer"

    def test_apply_promotion_with_negative_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = SecondHalfPricePromotion()
        with pytest.raises(ValueError) as e:
            promotion.apply_promotion(product, -10)
        assert str(e.value) == "Quantity must be non-negative"

    def test_apply_promotion_with_zero_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = SecondHalfPricePromotion()
        assert promotion.apply_promotion(product, 0) == 0

    def test_apply_promotion_with_quantity_of_one(self):
        product = Product("Test Product", 100, 100)
        promotion = SecondHalfPricePromotion()
        assert promotion.apply_promotion(product, 1) == 100

    def test_apply_promotion_with_odd_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = SecondHalfPricePromotion()
        assert promotion.apply_promotion(product, 3) == 250


class TestThirdOneFreePromotion:
    def test_apply_promotion(self):
        product = Product("Test Product", 100, 100)
        promotion = ThirdOneFreePromotion()
        assert promotion.apply_promotion(product, 10) == 800

    def test_apply_promotion_with_invalid_product(self):
        promotion = ThirdOneFreePromotion()
        with pytest.raises(ValueError) as e:
            promotion.apply_promotion("Test Product", 10)
        assert str(e.value) == "Product must be of type Product"

    def test_apply_promotion_with_invalid_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = ThirdOneFreePromotion()
        with pytest.raises(ValueError) as e:
            promotion.apply_promotion(product, "10")
        assert str(e.value) == "Quantity must be an integer"

    def test_apply_promotion_with_negative_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = ThirdOneFreePromotion()
        with pytest.raises(ValueError) as e:
            promotion.apply_promotion(product, -10)
        assert str(e.value) == "Quantity must be non-negative"

    def test_apply_promotion_with_zero_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = ThirdOneFreePromotion()
        assert promotion.apply_promotion(product, 0) == 0

    def test_apply_promotion_with_quantity_of_one(self):
        product = Product("Test Product", 100, 100)
        promotion = ThirdOneFreePromotion()
        assert promotion.apply_promotion(product, 1) == 100


class TestPercentDiscountPromotion:
    def test_apply_promotion(self):
        product = Product("Test Product", 100, 100)
        promotion = PercentDiscountPromotion(10)
        assert promotion.apply_promotion(product, 10) == 900

    def test_apply_promotion_with_invalid_product(self):
        promotion = PercentDiscountPromotion(10)
        with pytest.raises(ValueError) as e:
            promotion.apply_promotion("Test Product", 10)
        assert str(e.value) == "Product must be of type Product"

    def test_apply_promotion_with_invalid_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = PercentDiscountPromotion(10)
        with pytest.raises(ValueError) as e:
            promotion.apply_promotion(product, "10")
        assert str(e.value) == "Quantity must be an integer"

    def test_apply_promotion_with_negative_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = PercentDiscountPromotion(10)
        with pytest.raises(ValueError) as e:
            promotion.apply_promotion(product, -10)
        assert str(e.value) == "Quantity must be non-negative"

    def test_apply_promotion_with_zero_quantity(self):
        product = Product("Test Product", 100, 100)
        promotion = PercentDiscountPromotion(10)
        assert promotion.apply_promotion(product, 0) == 0

    def test_init_with_invalid_discount(self):
        with pytest.raises(ValueError, match="Discount must be a float"):
            PercentDiscountPromotion("10")

    def test_init_with_negative_discount(self):
        with pytest.raises(ValueError, match="Discount must be non-negative"):
            PercentDiscountPromotion(-10)