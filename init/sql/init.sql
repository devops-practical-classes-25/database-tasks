-- Создание таблицы авторов
CREATE TABLE author (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INTEGER NOT NULL
);

-- Создание таблицы книг
CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER NOT NULL,
    year_published INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE
);

-- Создание таблицы читателей
CREATE TABLE reader (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- Создание таблицы выдачи книг
CREATE TABLE loan (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    reader_id INTEGER NOT NULL,
    loan_date DATE NOT NULL,
    return_date DATE NULL,
    FOREIGN KEY (book_id) REFERENCES book(id) ON DELETE CASCADE,
    FOREIGN KEY (reader_id) REFERENCES reader(id) ON DELETE CASCADE
);

-- Наполнение таблицы author тестовыми данными
INSERT INTO author (name, birth_year) VALUES
('Лев Толстой', 1828),
('Фёдор Достоевский', 1821),
('Антон Чехов', 1860);

-- Наполнение таблицы book тестовыми данными
INSERT INTO book (title, author_id, year_published) VALUES
('Война и мир', 1, 1869),
('Преступление и наказание', 2, 1866),
('Чайка', 3, 1896);

-- Наполнение таблицы reader тестовыми данными
INSERT INTO reader (name, email) VALUES
('Иван Иванов', 'ivanov@example.com'),
('Мария Смирнова', 'smirnova@example.com'),
('Алексей Петров', 'petrov@example.com');

-- Наполнение таблицы loan тестовыми данными
INSERT INTO loan (book_id, reader_id, loan_date, return_date) VALUES
(1, 1, '2024-03-01', NULL), -- Книга еще не возвращена
(2, 2, '2024-02-20', '2024-03-10'), -- Книга возвращена
(3, 3, '2024-03-05', NULL); -- Книга еще не возвращена

-- SQL-запрос для получения списка книг, которые находятся у читателей на руках
SELECT 
    book.title AS "Название книги",
    reader.name AS "Читатель",
    loan.loan_date AS "Дата выдачи"
FROM loan
JOIN book ON loan.book_id = book.id
JOIN reader ON loan.reader_id = reader.id
WHERE loan.return_date IS NULL;