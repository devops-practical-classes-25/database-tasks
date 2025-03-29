# Задания для работы с СУБД

Репозиторий содержит тренировочные задания для работы с системами управления базами данных (СУБД). Целью этих заданий является практическое освоение принципов проектирования и нормализации баз данных, а также написание SQL-запросов для решения типичных задач.

Данный репозиторий включает набор практических задач, которые помогают закрепить навыки работы с базами данных. Задания охватывают такие темы, как:

1. Задание №1 - Библиотека - Создать схему базы данных
2. Задание №2 - Онлайн-магазин - Провести нормализацию базы данных
3. Задание №3 - Студенты - Проанализировать данные с использованием агрегатных функций и GROUP BY

## Зависимости для тестирования

Для тестирования базы данных используются следующие зависимости:

- **pytest**: для написания и запуска тестов.
- **SQLAlchemy**: для работы с базой данных.
- **psycopg2-binary**: драйвер для подключения к PostgreSQL.

Зависимости указаны в конфигурационном файле `pyproject.toml` и устанавливаются автоматически при выполнении команды:

```bash
poetry install
```
