import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from tests.config import Settings

CONN_STR_TEMPLATE = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"


@pytest.fixture(scope="session")
def db_engine():
    """Фикстура для создания движка SQLAlchemy."""
    settings = Settings()
    conn_str = CONN_STR_TEMPLATE.format(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        dbname=settings.POSTGRES_DB,
    )
    engine = create_engine(conn_str)

    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    init_script = None
    with open("./init/init.sql", "r") as file:
        init_script = file.read()
    session.execute(text(init_script))
    session.close()
    transaction.commit()
    connection.close()

    yield engine
    engine.dispose()  # Закрываем соединение после завершения тестов


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Фикстура для создания сессии SQLAlchemy."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session  # Возвращаем сессию для использования в тестах

    # Откатываем транзакцию и закрываем сессию после завершения теста
    session.close()
    transaction.rollback()
    connection.close()
