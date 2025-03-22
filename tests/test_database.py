import datetime
from sqlalchemy import text


def test_db_connection(db_session):
    """Проверяет наличие подключения к тестируемой базе данных, выполняя простой запрос"""
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


def test_author_data(db_session):
    """Проверяет корректность данных в таблице author"""
    result = db_session.execute(
        text(
            """
            SELECT name, birth_year FROM author
            ORDER BY name
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 3  # Должно быть три автора
    assert data[0] == ("Антон Чехов", 1860)
    assert data[1] == ("Фёдор Достоевский", 1821)
    assert data[2] == ("Лев Толстой", 1828)


def test_book_data(db_session):
    """Проверяет корректность данных в таблице book"""
    result = db_session.execute(
        text(
            """
            SELECT title, author_id, year_published FROM book
            ORDER BY title
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 3  # Должно быть три книги
    assert data[0] == ("Война и мир", 1, 1869)
    assert data[1] == ("Преступление и наказание", 2, 1866)
    assert data[2] == ("Чайка", 3, 1896)


def test_reader_data(db_session):
    """Проверяет корректность данных в таблице reader"""
    result = db_session.execute(
        text(
            """
            SELECT name, email FROM reader
            ORDER BY name
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 3  # Должно быть три читателя
    assert data[0] == ("Алексей Петров", "petrov@example.com")
    assert data[1] == ("Мария Смирнова", "smirnova@example.com")
    assert data[2] == ("Иван Иванов", "ivanov@example.com")


def test_loan_data(db_session):
    """Проверяет корректность данных в таблице loan"""
    result = db_session.execute(
        text(
            """
            SELECT book_id, reader_id, loan_date, return_date FROM loan
            ORDER BY loan_date
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 3  # Должно быть три записи о выдаче книг
    assert data[0] == (1, 1, datetime.date(2024, 3, 1), None)  # "Война и мир" - еще не возвращена
    assert data[1] == (2, 2, datetime.date(2024, 2, 20), datetime.date(2024, 3, 10))  # "Преступление и наказание" - возвращена
    assert data[2] == (3, 3, datetime.date(2024, 3, 5), None)  # "Чайка" - еще не возвращена


def test_books_with_loaned_status(db_session):
    """Проверяет, что список книг, которые находятся у читателей на руках, соответствует данным"""
    result = db_session.execute(
        text(
            """
            SELECT 
                book.title AS "Название книги",
                reader.name AS "Читатель",
                loan.loan_date AS "Дата выдачи"
            FROM loan
            JOIN book ON loan.book_id = book.id
            JOIN reader ON loan.reader_id = reader.id
            WHERE loan.return_date IS NULL
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 2  # Должно быть две строки, так как две книги еще не возвращены
    assert data[0] == ("Война и мир", "Иван Иванов", datetime.date(2024, 3, 1))
    assert data[1] == ("Чайка", "Алексей Петров", datetime.date(2024, 3, 5))


def test_books_returned(db_session):
    """Проверяет книги, которые были возвращены"""
    result = db_session.execute(
        text(
            """
            SELECT 
                book.title AS "Название книги",
                reader.name AS "Читатель",
                loan.loan_date AS "Дата выдачи",
                loan.return_date AS "Дата возврата"
            FROM loan
            JOIN book ON loan.book_id = book.id
            JOIN reader ON loan.reader_id = reader.id
            WHERE loan.return_date IS NOT NULL
            """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 1  # Только одна книга была возвращена
    assert data[0] == ("Преступление и наказание", "Мария Смирнова", datetime.date(2024, 2, 20), datetime.date(2024, 3, 10))


def test_books_loan_by_reader(db_session):
    """Проверяет, какие книги были выданы конкретному читателю"""
    reader_name = "Иван Иванов"
    result = db_session.execute(
        text(
            """
            SELECT 
                book.title AS "Название книги",
                loan.loan_date AS "Дата выдачи"
            FROM loan
            JOIN book ON loan.book_id = book.id
            JOIN reader ON loan.reader_id = reader.id
            WHERE reader.name = :reader_name AND loan.return_date IS NULL
            """,
            {"reader_name": reader_name}
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 1  # Иван Иванов взял одну книгу
    assert data[0] == ("Война и мир", datetime.date(2024, 3, 1))


def test_loaned_books_by_author(db_session):
    """Проверяет, какие книги определенного автора находятся на руках у читателей"""
    author_name = "Лев Толстой"
    result = db_session.execute(
        text(
            """
            SELECT 
                book.title AS "Название книги",
                reader.name AS "Читатель",
                loan.loan_date AS "Дата выдачи"
            FROM loan
            JOIN book ON loan.book_id = book.id
            JOIN reader ON loan.reader_id = reader.id
            JOIN author ON book.author_id = author.id
            WHERE author.name = :author_name AND loan.return_date IS NULL
            """,
            {"author_name": author_name}
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 1  # У Льва Толстого только одна книга на руках
    assert data[0] == ("Война и мир", "Иван Иванов", datetime.date(2024, 3, 1))

