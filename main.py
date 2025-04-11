class User:
    users_db = []  # Простий список для збереження користувачів

    def __init__(self, username, password, email):
        if not username:
            raise ValueError("Username cannot be empty")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not self.is_valid_email(email):
            raise ValueError("Invalid email address")

        # Перевірка наявності користувача з таким email
        for user in User.users_db:
            if user.email == email:
                raise ValueError(f"User with email {email} is already registered.")

        self.username = username
        self.password = password
        self.email = email
        self.orders = []


        User.users_db.append(self)

    def register(self):
        print(f"User {self.username} registered successfully.")

    def login(self, entered_password):
        if self.password == entered_password:
            print(f"User {self.username} logged in successfully.")
            return True
        else:
            print("Incorrect password!")
            return False

    def view_orders(self):
        return self.orders

    def add_order(self, order):
        self.orders.append(order)
        print(f"Order {order.order_id} added to user {self.username}'s orders.")

    @staticmethod
    def is_valid_email(email):

        return "@" in email and "." in email


class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        self.stock -= quantity
        print(f"{quantity} {self.name}(s) removed from stock. New stock: {self.stock}")

    def get_price(self):
        return self.price

    def restock(self, quantity):
        self.stock += quantity
        print(f"Restocked {quantity} {self.name}(s). New stock: {self.stock}")


class Order:
    def __init__(self, order_id, user):
        self.order_id = order_id
        self.user = user
        self.products = []
        self.total_amount = 0

    def add_product(self, product, quantity):
        self.products.append((product, quantity))
        product.update_stock(quantity)
        self.total_amount += product.get_price() * quantity
        print(f"Added {quantity} {product.name}(s) to order {self.order_id}. Total: {self.total_amount}")

    def remove_product(self, product):
        for p, q in self.products:
            if p == product:
                self.products.remove((p, q))
                self.total_amount -= p.get_price() * q
                p.restock(q)
                print(f"Removed {product.name} from order {self.order_id}. Total: {self.total_amount}")

    def calculate_total(self):
        print(f"Total for order {self.order_id}: {self.total_amount}")
        return self.total_amount

    def view_order_details(self):
        details = f"Order {self.order_id} details:\n"
        for product, quantity in self.products:
            details += f"{product.name} x{quantity} - {product.get_price() * quantity}\n"
        return details


class ShoppingCart:
    def __init__(self, user):
        self.user = user
        self.products = []

    def add_item(self, product, quantity):
        self.products.append((product, quantity))
        print(f"Added {quantity} {product.name}(s) to shopping cart.")

    def remove_item(self, product):
        for p, q in self.products:
            if p == product:
                self.products.remove((p, q))
                print(f"Removed {product.name} from shopping cart.")

    def clear_cart(self):
        self.products = []
        print("Shopping cart cleared.")

    def view_cart(self):
        details = "Shopping Cart Details:\n"
        for product, quantity in self.products:
            details += f"{product.name} x{quantity} - {product.get_price() * quantity}\n"
        return details

    def checkout(self):
        if not self.products:
            print("Cart is empty. Cannot checkout.")
            return
        total = sum([product.get_price() * quantity for product, quantity in self.products])
        print(f"Proceeding to checkout. Total amount: {total}")
        order = Order(order_id="ORD" + str(len(self.user.orders) + 1), user=self.user)
        for product, quantity in self.products:
            order.add_product(product, quantity)
        self.user.add_order(order)
        self.clear_cart()
        return order



if __name__ == "__main__":
    try:
        # Створення користувача
        user1 = User("john_doe", "password123", "john@example.com")
        user1.register()  # Реєстрація користувача

        # Логін користувача
        user1.login("password123")  # Вірний пароль
        user1.login("wrongpassword")  # Невірний пароль
    except ValueError as e:
        print(e)

    # Створення продуктів
    product1 = Product("Laptop", 1000.0, 10)
    product2 = Product("Phone", 500.0, 15)

    # Створення кошика покупок
    cart = ShoppingCart(user1)

    # Додавання товарів до кошика
    cart.add_item(product1, 2)
    cart.add_item(product2, 1)

    # Перегляд кошика
    print(cart.view_cart())

    # Оформлення замовлення
    order = cart.checkout()

    # Перегляд деталей замовлення
    print(order.view_order_details())

    # Перегляд замовлень користувача
    print(user1.view_orders())

    # Додавання ще одного товару в замовлення
    product3 = Product("Tablet", 300.0, 20)
    order.add_product(product3, 1)

    # Перегляд замовлення після додавання нового товару
    print(order.view_order_details())

    # Видалення товару з замовлення
    order.remove_product(product2)

    # Перегляд замовлення після видалення товару
    print(order.view_order_details())

    # Перегляд наявності товарів
    print(f"Stock of {product1.name}: {product1.stock}")
    print(f"Stock of {product2.name}: {product2.stock}")
    print(f"Stock of {product3.name}: {product3.stock}")
