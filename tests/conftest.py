import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from tests.config import Settings

CONN_STR_TEMPLATE = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

@pytest.fixture(scope="session")
def db_engine():
    settings = Settings()
    conn_str = CONN_STR_TEMPLATE.format(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        dbname=settings.POSTGRES_DB,
    )
    engine = create_engine(conn_str)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
    # Полная очистка базы перед каждым тестом
    with db_engine.connect() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
        connection.commit()

    # Инициализация тестовых данных
    init_path = Path(__file__).parent.parent / "init" / "init.sql"
    with db_engine.connect() as connection:
        with open(init_path, "r") as f:
            sql = f.read()
            connection.execute(text(sql))
        connection.commit()

    # Создание сессии для теста
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()