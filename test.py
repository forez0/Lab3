import unittest
from main import User, Product, Order, ShoppingCart


class TestECommerceSystem(unittest.TestCase):

    def test_user_registration(self):
        user = User("john_doe", "password123", "john@example.com")
        self.assertEqual(user.username, "john_doe")
        self.assertEqual(user.email, "john@example.com")

    def test_product_price(self):
        product = Product("Laptop", 1000.0, 10)
        self.assertEqual(product.get_price(), 1000.0)

    def test_order_total(self):
        user = User("john_doe", "password123", "john@example.com")
        product = Product("Laptop", 1000.0, 10)
        order = Order("ORD123", user)
        order.add_product(product, 2)
        self.assertEqual(order.calculate_total(), 2000.0)

    def test_add_remove_product_in_order(self):
        user = User("john_doe", "password123", "john@example.com")
        product = Product("Laptop", 1000.0, 10)
        order = Order("ORD123", user)
        order.add_product(product, 2)
        self.assertEqual(order.calculate_total(), 2000.0)
        order.remove_product(product)
        self.assertEqual(order.calculate_total(), 0.0)

    def test_shopping_cart(self):
        user = User("john_doe", "password123", "john@example.com")
        product = Product("Laptop", 1000.0, 10)
        cart = ShoppingCart(user)
        cart.add_item(product, 2)
        self.assertEqual(len(cart.products), 1)
        cart.remove_item(product)
        self.assertEqual(len(cart.products), 0)

    def test_checkout_process(self):
        user = User("john_doe", "password123", "john@example.com")
        product = Product("Laptop", 1000.0, 10)
        cart = ShoppingCart(user)
        cart.add_item(product, 2)
        order = cart.checkout()
        self.assertEqual(len(order.products), 1)
        self.assertEqual(order.calculate_total(), 2000.0)

    def test_user_order_association(self):
        user = User("john_doe", "password123", "john@example.com")
        product = Product("Laptop", 1000.0, 10)
        order = Order("ORD124", user)
        order.add_product(product, 1)
        user.add_order(order)
        self.assertIn(order, user.orders)

    def test_product_stock_update(self):
        user = User("john_doe", "password123", "john@example.com")
        product = Product("Laptop", 1000.0, 5)
        order = Order("ORD125", user)
        order.add_product(product, 2)
        self.assertEqual(product.stock, 3)

    def test_checkout_empty_cart(self):
        user = User("john_doe", "password123", "john@example.com")
        cart = ShoppingCart(user)
        order = cart.checkout()
        self.assertIsNone(order)

    def test_user_registration_with_empty_username(self):
        with self.assertRaises(ValueError):
            User("", "password123", "user@example.com")


if __name__ == '__main__':
    unittest.main()
