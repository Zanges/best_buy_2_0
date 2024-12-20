import pytest

from store import Store
from products import Product, NonStockedProduct, LimitedProduct


# test dependency is not working here
# i want to test the store class after the product class
# @pytest.mark.dependency(depends=["test_correct_product"])
def test_correct_store():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 5)
    store = Store([product1, product2])
    assert store.products == [product1, product2]


def test_add_product():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 5)
    store = Store([product1])
    store.add_product(product2)
    assert store.products == [product1, product2]


def test_add_product_already_exists():
    product1 = Product("Test Product 1", 10, 5)
    store = Store([product1])
    with pytest.raises(ValueError, match="Product already exists in the store"):
        store.add_product(product1)


def test_remove_product():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 5)
    store = Store([product1, product2])
    store.remove_product(product1)
    assert store.products == [product2]


def test_remove_product_not_exists():
    product1 = Product("Test Product 1", 10, 5)
    store = Store([product1])
    with pytest.raises(ValueError, match="Product does not exist in the store"):
        store.remove_product(Product("Test Product 2", 20, 5))


def test_get_total_quantity():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 5)
    store = Store([product1, product2])
    assert store.get_total_quantity() == 10


def test_get_all_products():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 5)
    store = Store([product1, product2])
    assert store.get_all_products() == [product1, product2]


def test_order():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 5)
    store = Store([product1, product2])
    assert store.order([(product1, 2), (product2, 3)]) == 80


def test_order_product_not_exists():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 5)
    store = Store([product1, product2])
    with pytest.raises(ValueError, match="Product does not exist in the store"):
        store.order([(Product("Test Product 3", 30, 5), 2), (product2, 3)])


def test_order_product_not_active():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 0)
    store = Store([product1, product2])
    with pytest.raises(ValueError, match="Product is not active"):
        store.order([(product1, 2), (product2, 3)])


def test_order_not_enough_quantity(capsys):
    product1 = Product("Test Product 1", 10, 1)
    product2 = Product("Test Product 2", 20, 5)
    store = Store([product1, product2])
    assert store.order([(product1, 2), (product2, 3)]) == 60
    printed = capsys.readouterr()
    assert printed.out == "Error buying Test Product 1, Price: 10, Quantity: 1, Promotion: None: Not enough quantity in stock\n"


def test_store_with_non_product():
    with pytest.raises(ValueError, match="All elements of products must be of type Product"):
        Store([1, 2, 3])


def test_add_product_with_non_product():
    store = Store([])
    with pytest.raises(ValueError, match="Product must be of type Product"):
        store.add_product(1)


def test_remove_product_with_non_product():
    store = Store([])
    with pytest.raises(ValueError, match="Product must be of type Product"):
        store.remove_product(1)


def test_order_with_non_product():
    store = Store([])
    with pytest.raises(ValueError, match="Product does not exist in the store"):
        store.order([(1, 2), (2, 3)])


def test_order_with_non_stocked_product():
    product1 = Product("Test Product 1", 10, 5)
    product2 = NonStockedProduct("Test Product 2", 20)
    store = Store([product1, product2])
    assert store.order([(product1, 2), (product2, 3)]) == 80


def test_store_with_limited_product(capsys):
    product1 = Product("Test Product 1", 10, 5)
    product2 = LimitedProduct("Test Product 2", 20, 15, 5)
    store = Store([product1, product2])
    store.order([(product2, 6)])
    printed = capsys.readouterr()
    assert printed.out == "Error buying Test Product 2, Price: 20, Quantity: 15, Promotion: None, Limit: 5: Quantity must be less than or equal to 5\n"


def test_add_two_stores():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 5)
    store1 = Store([product1])
    store2 = Store([product2])
    store3 = store1 + store2
    assert store3.products == [product1, product2]
    assert store1.products == [product1]
    assert store2.products == [product2]


def test_add_two_stores_with_non_product():
    store1 = Store([])
    store2 = Store([])
    store3 = store1 + store2
    assert store3.products == []


def test_in_operator():
    product1 = Product("Test Product 1", 10, 5)
    product2 = Product("Test Product 2", 20, 5)
    store = Store([product1, product2])
    assert product1 in store
    assert product2 in store
    assert Product("Test Product 3", 30, 5) not in store