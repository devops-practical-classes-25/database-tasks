import datetime

from sqlalchemy import text


def test_db_connection(db_session):
    """Проверяет наличие подключения к тестируемой базе данных выполняя простой запрос"""
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


def test_student(db_session):
    """Проверяет корректность данных в таблицах student, person, student_group и sex
    Выполняет SQL-запрос, который объединяет данные из этих таблиц, и проверяет,
    что результат соответствует ожидаемым данным.
    Ожидаемый результат: запрос должен вернуть две строки с данными о студентах.
    """
    result = db_session.execute(
        text(
            """
        SELECT ps.name AS student_name
            ,ps.birth_date
            ,sex.name AS sex_name
            ,sg.name AS group_name	  
        FROM public.student AS st
            JOIN public.person AS ps ON ps.id = st.person_id
            JOIN public.student_group AS sg on sg.id = st.student_group_id
            JOIN public.sex ON sex.id = ps.sex_id
        ORDER BY ps.name
    """
        )
    )

    assert result
    data = result.fetchall()
    assert len(data) == 2
    assert data[0] == ("Jane Dow", datetime.date(2001, 6, 15), "female", "test-25-2")
    assert data[1] == ("John Dow", datetime.date(2000, 1, 1), "male", "test-25-1")
