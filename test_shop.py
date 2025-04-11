import unittest
from main import User, Product, Order, ShoppingCart

class TestUser(unittest.TestCase):
    def setUp(self):
        User.users_db = []  # Очищення списку користувачів перед кожним тестом
        self.user = User("john_doe", "password123", "john@example.com")

    def test_register_user(self):
        self.assertEqual(self.user.username, "john_doe")
        self.assertEqual(self.user.email, "john@example.com")

    def test_login_success(self):
        self.assertTrue(self.user.login("password123"))

    def test_login_failure(self):
        self.assertFalse(self.user.login("wrongpassword"))

    def test_add_order(self):
        order = Order("ORD1", self.user)
        self.user.add_order(order)
        self.assertIn(order, self.user.view_orders())

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Laptop", 1000.0, 10)

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(self.product.price, 1000.0)
        self.assertEqual(self.product.stock, 10)

    def test_update_stock(self):
        self.product.update_stock(2)
        self.assertEqual(self.product.stock, 8)

    def test_restock(self):
        self.product.restock(5)
        self.assertEqual(self.product.stock, 15)

class TestOrder(unittest.TestCase):
    def setUp(self):
        User.users_db = []  # Очищення списку користувачів перед кожним тестом
        self.user = User("alice", "securepass", "alice@example.com")
        self.product = Product("Phone", 500.0, 5)
        self.order = Order("ORD100", self.user)

    def test_add_product(self):
        self.order.add_product(self.product, 2)
        self.assertEqual(self.order.total_amount, 1000.0)
        self.assertEqual(self.product.stock, 3)

    def test_remove_product(self):
        self.order.add_product(self.product, 2)
        self.order.remove_product(self.product)
        self.assertEqual(self.order.total_amount, 0.0)
        self.assertEqual(self.product.stock, 5)

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        User.users_db = []  # Очищення списку користувачів перед кожним тестом
        self.user = User("bob", "pass1234", "bob@example.com")
        self.product = Product("Tablet", 300.0, 10)
        self.cart = ShoppingCart(self.user)

    def test_add_item(self):
        self.cart.add_item(self.product, 2)
        self.assertEqual(len(self.cart.products), 1)

    def test_remove_item(self):
        self.cart.add_item(self.product, 2)
        self.cart.remove_item(self.product)
        self.assertEqual(len(self.cart.products), 0)

    def test_checkout(self):
        self.cart.add_item(self.product, 2)
        order = self.cart.checkout()
        self.assertEqual(len(self.user.view_orders()), 1)
        self.assertEqual(order.total_amount, 600.0)
        self.assertEqual(self.product.stock, 8)

if __name__ == '__main__':
    unittest.main()
