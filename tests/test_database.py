import datetime
from sqlalchemy import text


def test_db_connection(db_session):
    """Проверяет подключение к базе данных"""
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
    """Проверяет корректность данных в таблице Orders"""
    result = db_session.execute(
        text(
            """
            SELECT customer_id, order_date FROM "Orders"
            ORDER BY order_date
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 4
    assert data[0] == (1, datetime.date(2024, 3, 10))
    assert data[1] == (2, datetime.date(2024, 3, 12))
    assert data[2] == (1, datetime.date(2024, 3, 15))
    assert data[3] == (2, datetime.date(2024, 3, 16))


def test_orders_item_data(db_session):
    """Проверяет корректность данных в таблице Orders_Item"""
    result = db_session.execute(
        text(
            """
            SELECT order_id, product_id, quantity FROM Orders_Item
            ORDER BY order_id, product_id
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 4
    assert data[0] == (1, 1, 1)
    assert data[1] == (2, 2, 1)
    assert data[2] == (3, 1, 2)
    assert data[3] == (4, 3, 1)


def test_customer_orders(db_session):
    """Проверяет заказы конкретного клиента"""
    customer_email = "ivan@mail.com"
    result = db_session.execute(
        text(
            """
            SELECT 
                p.name AS product_name,
                oi.quantity,
                o.order_date
            FROM "Orders" o
            JOIN Customer c ON o.customer_id = c.id
            JOIN Orders_Item oi ON o.id = oi.order_id
            JOIN Product p ON oi.product_id = p.id
            WHERE c.email = :email
            """
        ),
        {"email": customer_email}
    )

    assert result
    data = result.fetchall()
    assert len(data) == 2
    assert data[0] == ("Телефон", 1, datetime.date(2024, 3, 10))
    assert data[1] == ("Телефон", 2, datetime.date(2024, 3, 15))


def test_order_totals(db_session):
    """Проверяет общую стоимость заказов"""
    result = db_session.execute(
        text(
            """
            SELECT 
                o.id AS order_id,
                SUM(oi.quantity * p.price) AS total
            FROM "Orders" o
            JOIN Orders_Item oi ON o.id = oi.order_id
            JOIN Product p ON oi.product_id = p.id
            GROUP BY o.id
            ORDER BY o.id
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 4
    assert data[0] == (1, 20000.00)
    assert data[1] == (2, 60000.00)
    assert data[2] == (3, 40000.00)
    assert data[3] == (4, 30000.00)


def test_popular_products(db_session):
    """Проверяет самые популярные товары"""
    result = db_session.execute(
        text(
            """
            SELECT 
                p.name,
                SUM(oi.quantity) AS total_quantity
            FROM Orders_Item oi
            JOIN Product p ON oi.product_id = p.id
            GROUP BY p.name
            ORDER BY total_quantity DESC
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 3
    assert data[0] == ("Телефон", 3)
    assert data[1] == ("Ноутбук", 1)
    assert data[2] == ("Планшет", 1)


def test_customer_spending(db_session):
    """Проверяет общие траты клиентов"""
    result = db_session.execute(
        text(
            """
            SELECT 
                c.name,
                SUM(oi.quantity * p.price) AS total_spent
            FROM Customer c
            JOIN "Orders" o ON c.id = o.customer_id
            JOIN Orders_Item oi ON o.id = oi.order_id
            JOIN Product p ON oi.product_id = p.id
            GROUP BY c.name
            ORDER BY total_spent DESC
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 2  # У Сергея нет заказов
    assert data[0] == ("Иван Петров", 60000.00)
    assert data[1] == ("Анна Иванова", 90000.00)