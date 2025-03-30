DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS menu_items CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- Создание таблицы клиентов
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Создание таблицы блюд
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Создание таблицы заказов
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10,2) DEFAULT 0.00
);

-- Создание таблицы состава заказа
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    menu_item_id INTEGER NOT NULL REFERENCES menu_items(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);

-- Хранимая процедура для создания заказа
CREATE OR REPLACE FUNCTION place_order(customer_id INT, item_ids INT[], quantities INT[]) RETURNS VOID AS $$
DECLARE
    new_order_id INT;
    i INT;
BEGIN
    -- Создаем новый заказ
    INSERT INTO orders (customer_id) VALUES (customer_id) RETURNING id INTO new_order_id;
    
    -- Добавляем блюда в заказ
    FOR i IN 1..array_length(item_ids, 1) LOOP
        INSERT INTO order_items (order_id, menu_item_id, quantity)
        VALUES (new_order_id, item_ids[i], quantities[i]);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Триггер для автоматического расчета стоимости заказа
CREATE OR REPLACE FUNCTION update_order_total() RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders
    SET total_price = (
        SELECT COALESCE(SUM(m.price * oi.quantity), 0)
        FROM order_items oi
        JOIN menu_items m ON oi.menu_item_id = m.id
        WHERE oi.order_id = NEW.order_id
    )
    WHERE id = NEW.order_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_order_total
AFTER INSERT OR UPDATE ON order_items
FOR EACH ROW
EXECUTE FUNCTION update_order_total();

-- Наполнение базы тестовыми данными
INSERT INTO customers (name, email) VALUES ('Иван Иванов', 'ivan@example.com'), ('Мария Смирнова', 'maria@example.com');
INSERT INTO menu_items (name, price) VALUES ('Пицца', 500.00), ('Салат', 250.00), ('Суп', 300.00);

-- Тестовый вызов хранимой процедуры
SELECT place_order(1, ARRAY[1, 2], ARRAY[1, 2]);
