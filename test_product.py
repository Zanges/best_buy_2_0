import pytest

from products import Product


def test_correct_product():
    product = Product("Test Product", 10, 5)
    assert product.name == "Test Product"
    assert product.price == 10
    assert product.quantity == 5
    assert product.active == True


def test_zero_quantity():
    product = Product("Test Product", 10, 0)
    assert product.active == False


def test_negative_price():
    with pytest.raises(ValueError, match="Price must be non-negative"):
        product = Product("Test Product", -10, 5)


def test_negative_quantity():
    with pytest.raises(ValueError, match="Quantity must be non-negative"):
        product = Product("Test Product", 10, -5)


def test_empty_name():
    with pytest.raises(ValueError, match="Name must be a non empty string"):
        product = Product("", 10, 5)


def test_price_not_number():
    with pytest.raises(ValueError, match="Price must be a number"):
        product = Product("Test Product", "10", 5)


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