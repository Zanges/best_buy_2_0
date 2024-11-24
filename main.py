from products import Product
from store import Store


SEPARATOR = "-" * 10


def initialize_best_buy() -> Store:
    """ Initializes the Best Buy store """
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250)
    ]
    return Store(product_list)


def list_all_products_command(store: Store) -> list[Product]:
    """ Lists all products in the store and returns them """
    print(SEPARATOR)
    products = store.get_all_products()
    for index, product in enumerate(products):
        print(f"{index + 1}. {product}")
    print(SEPARATOR)
    return products


def get_valid_product_number(highest_product_number: int) -> int or None:
    """ Asks the user for a valid product number """
    while True:
        product_number = input("Which product # do you want? ")
        if product_number == "":
            return None
        try:
            product_number = int(product_number) - 1
        except ValueError:
            print("Invalid product number")
            continue
        if product_number < 0 or product_number >= highest_product_number:
            print("Invalid product number")
            continue
        return product_number


def get_valid_quantity() -> int:
    """ Asks the user for a valid quantity """
    while True:
        quantity = input("What amount do you want? ")
        try:
            quantity = int(quantity)
        except ValueError:
            print("Invalid quantity")
            continue
        if quantity < 0:
            print("Invalid quantity")
            continue
        return quantity


def order_command(store: Store) -> None:
    """ Orders products from the store """
    print("When you want to finish order, enter empty text.")
    product_list = list_all_products_command(store)
    order_list = []
    while True:
        product_number = get_valid_product_number(len(product_list))
        if product_number is None:
            break
        product = product_list[product_number]

        quantity = get_valid_quantity()
        order_list.append((product, quantity))

    print(SEPARATOR)
    try:
        total_cost = store.order(order_list)
        print(f"Total cost: {total_cost}")
    except ValueError as e:
        print(f"Error ordering: {e}")
        print("Order cancelled")
    print(SEPARATOR)


def store_total_quantity_command(store: Store) -> int:
    """ Shows the total quantity in the store and returns it """
    print(SEPARATOR)
    total_quantity = store.get_total_quantity()
    print(f"Total quantity: {total_quantity}")
    print(SEPARATOR)
    return total_quantity


menu_options = [
    {
        "name": "List all products in store",
        "function": list_all_products_command
    },
    {
        "name": "Show total amount in store",
        "function": store_total_quantity_command
    },
    {
        "name": "Order products",
        "function": order_command
    },
    {
        "name": "Quit",
        "function": lambda store: exit()
    }
]


def show_menu(store: Store) -> None:
    """ Shows the menu and asks for user input """
    while True:
        print(SEPARATOR)
        print("Menu:")
        print(SEPARATOR)
        for index, option in enumerate(menu_options):
            print(f"{index + 1}. {option['name']}")
        choice = input("What do you want to do? ")
        try:
            choice = int(choice) - 1
        except ValueError:
            print("Invalid choice")
            continue
        if choice < 0 or choice >= len(menu_options):
            print("Invalid choice")
            continue
        option = menu_options[choice]
        option["function"](store)


def main():
    best_buy = initialize_best_buy()
    show_menu(best_buy)


if __name__ == "__main__":
    main()