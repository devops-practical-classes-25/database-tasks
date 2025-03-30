import pytest
from sqlalchemy import text

def test_db_connection(db_session):
    """Проверяет наличие подключения к тестируемой базе данных, выполняя простой запрос"""
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

def test_insert_customer(db_session):
    """Проверяет добавление клиента"""
    db_session.execute(text("INSERT INTO customers (name, email) VALUES ('Тестовый Клиент', 'test@example.com')"))
    db_session.commit()
    result = db_session.execute(text("SELECT name, email FROM customers WHERE email = 'test@example.com'"))
    data = result.fetchone()
    assert data == ('Тестовый Клиент', 'test@example.com')

def test_insert_menu_item(db_session):
    """Проверяет добавление блюда в меню"""
    db_session.execute(text("INSERT INTO menu_items (name, price) VALUES ('Тестовое блюдо', 150.00)"))
    db_session.commit()
    result = db_session.execute(text("SELECT name, price FROM menu_items WHERE name = 'Тестовое блюдо'"))
    data = result.fetchone()
    assert data == ('Тестовое блюдо', 150.00)

def test_create_order(db_session):
    """Проверяет создание заказа и корректность расчета стоимости"""

    db_session.execute(text("INSERT INTO customers (name, email) VALUES ('Покупатель', 'customer@example.com')"))
    
    db_session.execute(text("INSERT INTO menu_items (name, price) VALUES ('Пицца', 500.00), ('Салат', 250.00)"))
    db_session.commit()

    menu_items = db_session.execute(text("SELECT id, name, price FROM menu_items")).fetchall()
    print("Содержимое menu_items:", menu_items)  

    pizza_id = None
    salad_id = None
    for item in menu_items:
        if item[1] == "Пицца":
            pizza_id = item[0]
        elif item[1] == "Салат":
            salad_id = item[0]

    assert pizza_id is not None, "ID Пиццы не найден!"
    assert salad_id is not None, "ID Салата не найден!"

    db_session.execute(text("INSERT INTO orders (customer_id) VALUES (1)"))
    db_session.commit()

    order_id = db_session.execute(text("SELECT id FROM orders ORDER BY id DESC LIMIT 1")).scalar()
    assert order_id is not None, "ID заказа не найден!"

    db_session.execute(
        text("INSERT INTO order_items (order_id, menu_item_id, quantity) VALUES (:order_id, :pizza_id, 1), (:order_id, :salad_id, 2)"),
        {"order_id": order_id, "pizza_id": pizza_id, "salad_id": salad_id}
    )
    db_session.commit()

    order_items = db_session.execute(text("SELECT * FROM order_items")).fetchall()
    print("Содержимое order_items:", order_items)

    result = db_session.execute(text("SELECT id, customer_id, total_price FROM orders WHERE id = :order_id"),
                                {"order_id": order_id})
    order_data = result.fetchone()
    print("Содержимое orders:", order_data)

    assert order_data is not None, "Заказ не найден!"
    
    expected_total_price = 500.00 * 1 + 250.00 * 2
    assert order_data[2] == expected_total_price, f"Ожидалось {expected_total_price}, а получено {order_data[2]}"

def test_place_order_procedure(db_session):
    """Проверяет хранимую процедуру place_order"""
    db_session.execute(text("SELECT place_order(1, ARRAY[1, 2], ARRAY[1, 1])"))
    db_session.commit()
    
    result = db_session.execute(text("SELECT COUNT(*) FROM orders WHERE customer_id = 1"))
    count_orders = result.scalar()
    assert count_orders == 2
