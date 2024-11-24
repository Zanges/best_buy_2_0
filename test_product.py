import sys

import pytest

from products import Product, NonStockedProduct, LimitedProduct


@pytest.mark.dependency(name="test_correct_product")
def test_correct_product():
    product = Product("Test Product", 10, 5)
    assert product.name == "Test Product"
    assert product.price == 10
    assert product.quantity == 5
    assert product.active == True


@pytest.mark.dependency(depends=["test_correct_product"])
def test_zero_quantity():
    product = Product("Test Product", 10, 0)
    assert product.active == False


@pytest.mark.dependency(depends=["test_correct_product"])
def test_negative_price():
    with pytest.raises(ValueError, match="Price must be non-negative"):
        product = Product("Test Product", -10, 5)


@pytest.mark.dependency(depends=["test_correct_product"])
def test_negative_quantity():
    with pytest.raises(ValueError, match="Quantity must be non-negative"):
        product = Product("Test Product", 10, -5)


@pytest.mark.dependency(depends=["test_correct_product"])
def test_empty_name():
    with pytest.raises(ValueError, match="Name must be a non empty string"):
        product = Product("", 10, 5)


@pytest.mark.dependency(depends=["test_correct_product"])
def test_price_not_number():
    with pytest.raises(ValueError, match="Price must be a number"):
        product = Product("Test Product", "10", 5)


@pytest.mark.dependency(depends=["test_correct_product"])
def test_quantity_not_integer():
    with pytest.raises(ValueError, match="Quantity must be an integer"):
        product = Product("Test Product", 10, 5.5)


def test_get_quantity():
    product = Product("Test Product", 10, 5)
    assert product.get_quantity() == 5


def test_set_quantity():
    product = Product("Test Product", 10, 5)
    product.set_quantity(10)
    assert product.quantity == 10
    assert product.active == True


def test_set_quantity_zero():
    product = Product("Test Product", 10, 5)
    product.set_quantity(0)
    assert product.active == False


def test_set_quantity_from_zero():
    product = Product("Test Product", 10, 0)
    product.set_quantity(5)
    assert product.active == False


def test_set_quantity_negative():
    product = Product("Test Product", 10, 5)
    with pytest.raises(ValueError, match="New quantity must be non-negative"):
        product.set_quantity(-5)


def test_set_quantity_not_integer():
    product = Product("Test Product", 10, 5)
    with pytest.raises(ValueError, match="New quantity must be an integer"):
        product.set_quantity(5.5)


def test_is_active():
    product = Product("Test Product", 10, 5)
    assert product.is_active() == True


def test_activate():
    product = Product("Test Product", 10, 0)
    product.activate()
    assert product.active == True


def test_deactivate():
    product = Product("Test Product", 10, 5)
    product.deactivate()
    assert product.active == False


def test_str():
    product = Product("Test Product", 10, 5)
    assert str(product) == "Test Product, Price: 10, Quantity: 5"


def test_show():
    product = Product("Test Product", 10, 5)
    assert product.show() == "Test Product, Price: 10, Quantity: 5"
    assert product.show() == str(product)


def test_buy():
    product = Product("Test Product", 10, 5)
    assert product.buy(3) == 30
    assert product.quantity == 2
    assert product.active == True


def test_buy_all():
    product = Product("Test Product", 10, 5)
    assert product.buy(5) == 50
    assert product.active == False
    assert product.quantity == 0


def test_buy_more_than_quantity():
    product = Product("Test Product", 10, 5)
    with pytest.raises(ValueError, match="Not enough quantity in stock"):
        product.buy(6)


def test_buy_negative_quantity():
    product = Product("Test Product", 10, 5)
    with pytest.raises(ValueError, match="Quantity must be non-negative"):
        product.buy(-5)


def test_buy_not_integer():
    product = Product("Test Product", 10, 5)
    with pytest.raises(ValueError, match="Quantity must be an integer"):
        product.buy(5.5)


def test_non_stocked_product():
    product = NonStockedProduct("Test Product", 10)
    assert product.name == "Test Product"
    assert product.price == 10
    assert product.quantity == sys.maxsize
    assert product.active == True


def test_non_stocked_product_set_quantity():
    product = NonStockedProduct("Test Product", 10)
    with pytest.raises(ValueError, match="Cannot set quantity for non stocked product"):
        product.set_quantity(5)
    assert product.quantity == sys.maxsize
    assert product.active == True


def test_non_stocked_product_buy():
    product = NonStockedProduct("Test Product", 10)
    assert product.buy(5) == 50
    assert product.quantity == sys.maxsize
    assert product.active == True
    assert product.buy(10) == 100
    assert product.quantity == sys.maxsize
    assert product.active == True
    assert product.buy(10**10) == 10**11
    assert product.quantity == sys.maxsize
    assert product.active == True


def test_non_stocked_product_buy_negative_quantity():
    product = NonStockedProduct("Test Product", 10)
    with pytest.raises(ValueError, match="Quantity must be non-negative"):
        product.buy(-5)


def test_non_stocked_product_buy_not_integer():
    product = NonStockedProduct("Test Product", 10)
    with pytest.raises(ValueError, match="Quantity must be an integer"):
        product.buy(5.5)


def test_non_stocked_product_str():
    product = NonStockedProduct("Test Product", 10)
    assert str(product) == "Test Product, Price: 10, Quantity: ∞"


def test_non_stocked_product_show():
    product = NonStockedProduct("Test Product", 10)
    assert product.show() == "Test Product, Price: 10, Quantity: ∞"
    assert product.show() == str(product)


def test_limited_product():
    product = LimitedProduct("Test Product", 10, 5, 10)
    assert product.name == "Test Product"
    assert product.price == 10
    assert product.quantity == 5
    assert product.active == True
    assert product.limit == 10


def test_limited_product_buy():
    product = LimitedProduct("Test Product", 10, 5, 10)
    assert product.buy(5) == 50
    assert product.quantity == 0
    assert product.active == False


def test_limited_product_buy_more_than_limit():
    product = LimitedProduct("Test Product", 10, 50, 10)
    with pytest.raises(ValueError, match="Quantity must be less than or equal to 10"):
        product.buy(11)


def test_limited_product_str():
    product = LimitedProduct("Test Product", 10, 5, 10)
    assert str(product) == "Test Product, Price: 10, Quantity: 5, Limit: 10"


def test_limited_product_show():
    product = LimitedProduct("Test Product", 10, 5, 10)
    assert product.show() == "Test Product, Price: 10, Quantity: 5, Limit: 10"
    assert product.show() == str(product)


def test_limited_product_set_limit():
    product = LimitedProduct("Test Product", 10, 5, 10)
    product.set_limit(20)
    assert product.limit == 20


def test_limited_product_set_limit_negative():
    product = LimitedProduct("Test Product", 10, 5, 10)
    with pytest.raises(ValueError, match="Limit must be non-negative"):
        product.set_limit(-20)


def test_limited_product_set_limit_not_integer():
    product = LimitedProduct("Test Product", 10, 5, 10)
    with pytest.raises(ValueError, match="Limit must be an integer"):
        product.set_limit(20.5)


def test_get_quantity_limited_product():
    product = LimitedProduct("Test Product", 10, 5, 10)
    assert product.get_quantity() == 5