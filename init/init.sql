-- Удаление данных перед вставкой, сброс ID
TRUNCATE TABLE Orders_Item RESTART IDENTITY CASCADE;
TRUNCATE TABLE Orders RESTART IDENTITY CASCADE;
TRUNCATE TABLE Product RESTART IDENTITY CASCADE;
TRUNCATE TABLE Customer RESTART IDENTITY CASCADE;

-- 1. Создание таблицы клиентов
CREATE TABLE IF NOT EXISTS Customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- 2. Создание таблицы товаров
CREATE TABLE IF NOT EXISTS Product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0)
);

-- 3. Создание таблицы заказов
CREATE TABLE IF NOT EXISTS Orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE
);

-- 4. Создание таблицы позиций заказа
CREATE TABLE IF NOT EXISTS Orders_Item (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(id) ON DELETE RESTRICT
);

-- 5. Наполнение таблицы клиентов тестовыми данными
INSERT INTO Customer (name, email) VALUES
('Иван Петров', 'ivan@mail.com'),
('Анна Иванова', 'anna@mail.com'),
('Сергей Сидоров', 'sergey@mail.com')
ON CONFLICT (email) DO NOTHING;

-- 6. Наполнение таблицы товаров тестовыми данными
INSERT INTO Product (name, price) VALUES
('Телефон', 20000.00),
('Ноутбук', 60000.00),
('Планшет', 30000.00),
('Наушники', 5000.00)
ON CONFLICT (name) DO NOTHING;

-- 7. Наполнение таблицы заказов тестовыми данными
INSERT INTO Orders (customer_id, order_date) VALUES
(1, '2024-03-10'),
(2, '2024-03-12'),
(1, '2024-03-15'),
(2, '2024-03-16')
ON CONFLICT DO NOTHING;

-- 8. Наполнение таблицы позиций заказа тестовыми данными
INSERT INTO Orders_Item (order_id, product_id, quantity) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 1, 2),
(4, 3, 1)
ON CONFLICT DO NOTHING;

-- 9. SQL-запрос: список заказов с информацией о клиентах и товарах
SELECT 
    o.id AS order_id,
    c.name AS customer_name,
    p.name AS product_name,
    oi.quantity,
    p.price,
    (oi.quantity * p.price) AS total_price,
    o.order_date
FROM 
    Orders o
JOIN 
    Customer c ON o.customer_id = c.id
JOIN 
    Orders_Item oi ON o.id = oi.order_id
JOIN 
    Product p ON oi.product_id = p.id;

