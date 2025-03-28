import datetime
from sqlalchemy import text


def test_db_connection(db_session):
    """Проверяет наличие подключения к тестируемой базе данных, выполняя простой запрос"""
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


def test_customer_data(db_session):
    """Проверяет корректность данных в таблице Customer"""
    result = db_session.execute(
        text(
            """
            SELECT name, email FROM Customer
            ORDER BY name
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 3
    assert data[0] == ("Анна Иванова", "anna@mail.com")
    assert data[1] == ("Иван Петров", "ivan@mail.com")
    assert data[2] == ("Сергей Сидоров", "sergey@mail.com")


def test_product_data(db_session):
    """Проверяет корректность данных в таблице Product"""
    result = db_session.execute(
        text(
            """
            SELECT name, price FROM Product
            ORDER BY name
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 4
    assert data[0] == ("Наушники", 5000.00)
    assert data[1] == ("Ноутбук", 60000.00)
    assert data[2] == ("Планшет", 30000.00)
    assert data[3] == ("Телефон", 20000.00)


def test_order_data(db_session):
    """Проверяет данные в таблице orders"""
    result = db_session.execute(
        text("SELECT customer_id, order_date FROM orders ORDER BY order_date")
    )
    data = result.fetchall()
    assert len(data) == 4
    assert data[0] == (1, datetime.date(2024, 3, 10))
    assert data[1] == (2, datetime.date(2024, 3, 12))
    assert data[2] == (1, datetime.date(2024, 3, 15))
    assert data[3] == (2, datetime.date(2024, 3, 16))


def test_orders_item_data(db_session):
    """Проверяет данные в таблице orders_item"""
    result = db_session.execute(
        text("SELECT order_id, product_id, quantity FROM orders_item ORDER BY order_id")
    )
    data = result.fetchall()
    assert len(data) == 4
    assert data[0] == (1, 1, 1)
    assert data[1] == (2, 2, 1)
    assert data[2] == (3, 1, 2)
    assert data[3] == (4, 3, 1)


def test_customer_orders(db_session):
    """Проверяет заказы клиента"""
    result = db_session.execute(
        text("""
            SELECT p.name, oi.quantity, o.order_date 
            FROM orders o
            JOIN customer c ON o.customer_id = c.id
            JOIN orders_item oi ON o.id = oi.order_id
            JOIN product p ON oi.product_id = p.id
            WHERE c.email = :email
            ORDER BY o.order_date
        """),
        {"email": "ivan@mail.com"}
    )
    data = result.fetchall()
    assert len(data) == 2
    assert data[0] == ("Телефон", 1, datetime.date(2024, 3, 10))
    assert data[1] == ("Телефон", 2, datetime.date(2024, 3, 15))


def test_order_totals(db_session):
    """Проверяет общую стоимость заказов"""
    result = db_session.execute(
        text("""
            SELECT o.id, SUM(oi.quantity * p.price) 
            FROM orders o
            JOIN orders_item oi ON o.id = oi.order_id
            JOIN product p ON oi.product_id = p.id
            GROUP BY o.id
            ORDER BY o.id
        """)
    )
    data = result.fetchall()
    assert len(data) == 4
    assert data[0] == (1, 20000.0)
    assert data[1] == (2, 60000.0)
    assert data[2] == (3, 40000.0)
    assert data[3] == (4, 30000.0)


def test_popular_products(db_session):
    """Проверяет самые популярные товары"""
    result = db_session.execute(
        text("""
            SELECT 
                p.name,
                SUM(oi.quantity) AS total_quantity
            FROM orders_item oi
            JOIN product p ON oi.product_id = p.id
            GROUP BY p.name
            ORDER BY total_quantity DESC, p.name  -- Сортировка по количеству и имени
        """)
    )
    data = result.fetchall()
    assert len(data) == 3
    assert data[0] == ("Телефон", 3)
    assert data[1] == ("Ноутбук", 1)
    assert data[2] == ("Планшет", 1)

def test_customer_spending(db_session):
    """Проверяет траты клиентов"""
    result = db_session.execute(
        text("""
            SELECT c.name, SUM(oi.quantity * p.price)
            FROM customer c
            JOIN orders o ON c.id = o.customer_id
            JOIN orders_item oi ON o.id = oi.order_id
            JOIN product p ON oi.product_id = p.id
            GROUP BY c.name
            ORDER BY SUM(oi.quantity * p.price) DESC
        """)
    )
    data = result.fetchall()
    assert len(data) == 2
    assert data[0] == ("Анна Иванова", 90000.0)
    assert data[1] == ("Иван Петров", 60000.0)