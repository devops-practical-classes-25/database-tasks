import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.config import Settings

CONN_STR_TEMPLATE = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"


@pytest.fixture(scope="session")
def db_engine():
    """Фикстура для создания движка SQLAlchemy."""
    settings = Settings()
    conn_str = CONN_STR_TEMPLATE.format(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
    )
    engine = create_engine(conn_str)
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
