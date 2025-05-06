DROP TABLE IF EXISTS orders_item CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS customer CASCADE;

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customer(id),
    order_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE orders_item (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES product(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);

INSERT INTO customer (name, email) VALUES
('Иван Петров', 'ivan@mail.com'),
('Анна Иванова', 'anna@mail.com'),
('Сергей Сидоров', 'sergey@mail.com');

INSERT INTO product (name, price) VALUES
('Телефон', 20000.00),
('Ноутбук', 60000.00),
('Планшет', 30000.00),
('Наушники', 5000.00);

INSERT INTO orders (customer_id, order_date) VALUES
(99, '2024-03-10'),
(2, '2024-03-12'),
(1, '2024-03-15'),
(2, '2024-03-16');

INSERT INTO orders_item (order_id, product_id, quantity) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 1, 2),
(4, 3, 1);

SELECT 
    o.id AS order_id,
    c.name AS customer_name,
    p.name AS product_name,
    oi.quantity,
    p.price,
    (oi.quantity * p.price) AS total_price,
    o.order_date
FROM 
    orders o
JOIN 
    Customer c ON o.customer_id = c.id
JOIN 
    orders_item oi ON o.id = oi.order_id
JOIN 
    product p ON oi.product_id = p.id;