import datetime
from sqlalchemy import text

def test_db_connection(db_session):
    """Проверяет наличие подключения к тестируемой базе данных, выполняя простой запрос"""
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

def test_students_data(db_session):
    """Проверка данных студентов"""
    result = db_session.execute(
        text("SELECT name, group_name FROM students ORDER BY id")
    )
    data = result.fetchall()
    assert data == [
        ('Иван Петров', 'РИС'),
        ('Анна Иванова', 'Юриспруденция'),
        ('Сергей Смирнов', 'РИС'),
        ('Мария Кузнецова', 'Дизайн'),
        ('Алексей Васильев', 'Юриспруденция')
    ]

def test_courses_data(db_session):
    """Проверка данных курсов"""
    result = db_session.execute(
        text("SELECT name FROM courses ORDER BY id")
    )
    data = result.fetchall()
    assert data == [('Математика',), ('Физика',), ('История',)]

def test_grades_data(db_session):
    """Проверка данных оценок"""
    result = db_session.execute(
        text("SELECT student_id, course_id, grade FROM grades ORDER BY id")
    )
    data = result.fetchall()
    assert len(data) == 15
    assert (1, 1, 10) in data
    assert (5, 2, 8) in data

def test_avg_student_grades(db_session):
    """Проверка среднего балла студентов"""
    result = db_session.execute(text("""
        SELECT s.name, ROUND(AVG(g.grade), 2)
        FROM students s
        LEFT JOIN grades g ON s.id = g.student_id
        GROUP BY s.id
        ORDER BY AVG(g.grade) DESC
    """))
    data = result.fetchall()
    
    ivan = next(x for x in data if x[0] == 'Иван Петров')
    assert float(ivan[1]) == 9.33
    
    maria = next(x for x in data if x[0] == 'Мария Кузнецова')
    assert maria[1] == 9.0

def test_avg_course_grades(db_session):
    """Проверка среднего балла по курсам"""
    result = db_session.execute(text("""
        SELECT c.name, ROUND(AVG(g.grade), 2)
        FROM courses c
        LEFT JOIN grades g ON c.id = g.course_id
        GROUP BY c.id
        ORDER BY c.id
    """))
    data = result.fetchall()
    
    assert (data[0][0], float(data[0][1])) == ('Математика', 9.33)
    assert (data[1][0], float(data[1][1])) == ('Физика', 8.6)
    assert (data[2][0], float(data[2][1])) == ('История', 8.0)

def test_group_students_count(db_session):
    """Проверка количества студентов в группах"""
    result = db_session.execute(text("""
        SELECT group_name, COUNT(*)
        FROM students
        GROUP BY group_name
        ORDER BY COUNT(*) DESC
    """))
    data = result.fetchall()
    
    assert data == [
        ('РИС', 2),
        ('Юриспруденция', 2),
        ('Дизайн', 1)
    ]

def test_top_student(db_session):
    """Проверка студента с максимальным средним баллом"""
    result = db_session.execute(text("""
        SELECT s.name, ROUND(AVG(g.grade), 2)
        FROM students s
        JOIN grades g ON s.id = g.student_id
        GROUP BY s.id
        ORDER BY AVG(g.grade) DESC
        LIMIT 1
    """))
    top_student = result.fetchone()
    
    assert float(top_student[1]) == 9.33
    assert top_student[0] in ['Иван Петров', 'Анна Иванова']

def test_students_without_history_grades(db_session):
    """Проверка студентов без оценок по истории"""
    result = db_session.execute(text("""
        SELECT s.name
        FROM students s
        WHERE NOT EXISTS (
            SELECT 1
            FROM grades g
            JOIN courses c ON g.course_id = c.id
            WHERE g.student_id = s.id AND c.name = 'История'
        )
    """))
    data = [row[0] for row in result.fetchall()]
    assert len(data) == 1

def test_most_tens_course(db_session):
    """Проверка курса с наибольшим количеством 10"""
    result = db_session.execute(text("""
        SELECT c.name, COUNT(*)
        FROM courses c
        JOIN grades g ON c.id = g.course_id
        WHERE g.grade = 10
        GROUP BY c.id
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """))
    course = result.fetchone()
    
    assert course == ('Математика', 3)