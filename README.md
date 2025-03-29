# Задание №3 - Анализ данных с использованием агрегатных функций и GROUP BY

**Цель**: Научиться использовать агрегатные функции (COUNT, SUM, AVG) и группировку данных для анализа информации в БД.

Создать базу данных для учета студентов, курсов и их оценок.

**Требования:**

1. Создать таблицы:

   + students (id, name, group_name).
   + courses (id, name).
   + grades (id, student_id, course_id, grade, date).

2. Заполнить таблицы в соотвествие с данными (5 студентов, 3 курса, 10 оценок):

    ```
    Иван Петров (группа РИС): Отличник по математике - получил две "10" и одну "8" по физике. Его средний балл 9.33 - лучший в группе. 

    Анна Иванова (группа Юриспруденция): Стабильная хорошистка - имеет "9" по математике (дважды) и "10" по истории. Средний балл - 9.25.

    Сергей Смирнов (группа РИС): Силен в гуманитарных науках - "9" по истории, но с физикой сложнее ("7" и "10"). Средний балл - 8.67.

    Мария Кузнецова (группа Дизайн): Ярко выраженный технарь - идеальные "10" по математике и физике, но по истории всего "7". Средний балл - 9.0.

    Алексей Васильев (группа Юриспруденция): Испытывает трудности - самая низкая оценка "6" по истории, "8" по математике и физике. Средний балл - 7.33.
    ```

3. Написать SQL-запросы для решения задач:

    + Найти средний балл каждого студента.
    + Найти средний балл по каждому курсу.
    + Найти количество студентов в каждой группе.
    + Найти студента с максимальным средним баллом.
    + Найти студентов, у которых нет оценок по определенному курсу.
    + Найти курс с наибольшим количеством оценок "10".

## Теоретическая информация

**Агрегатные функции** -Агрегатные функции выполняют вычисления на наборе значений и возвращают одно значение:

1. COUNT() - подсчитывает количество строк

2. SUM() - вычисляет сумму значений

3. AVG() - вычисляет среднее значение

4. MAX() - находит максимальное значение

5. MIN() - находит минимальное значение

**Группировка данных (GROUP BY)** - оператор GROUP BY группирует строки, имеющие одинаковые значения в указанных столбцах, в сводные строки. Часто используется с агрегатными функциями

**Соединение таблиц (JOIN)** - JOIN используется для объединения строк из двух или более таблиц на основе связанного между ними столбца.

Основные типы JOIN:

1. INNER JOIN - возвращает записи, имеющие соответствие в обеих таблицах

2. LEFT JOIN - возвращает все записи из левой таблицы и соответствующие записи из правой

3. RIGHT JOIN - возвращает все записи из правой таблицы и соответствующие записи из левой

4. FULL JOIN - возвращает записи при наличии соответствия в любой из таблиц

## Инструкция по запуску

### 1. Запуск PostgreSQL и pgAdmin в Docker-контейнерах

Для запуска PostgreSQL и pgAdmin используйте Docker Compose. Убедитесь, что у вас установлены Docker и Docker Compose.

1. Убедитесь, что в корне проекта присутствует и заполнен файл .env.local.
2. Убедитесь, что порты 5433 и 5434 свободны на вашем компьютере.
3. Запустите контейнеры:

```bash
docker compose -f docker-compose.local.yml --env-file=.env.local  up -d
```

Это команда:
- Запускает контейнеры PostgreSQL и pgAdmin.
- При первом запуске контейнера с PostgreSQL применяется SQL-скрипт init/sql/init.sql для инициализации базы данных. В создаваемой базе данных выполняются все команды указанные в файле init.sql.

После запуска:
- PostgreSQL будет доступен на localhost:5433.
- pgAdmin будет доступен на localhost:5434.
- Подключитесь к PostgreSQL через pgAdmin, используя:
    * Host: postgres
    * Port: 5432
    * Username: postgres
    * Password: postgres
    * Database: postgres

### 2. Остановка контейнеров

Чтобы остановить и удалить контейнеры, выполните:

```bash
docker compose -f docker-compose.local.yml --env-file=.env.local  down
```

Чтобы остановить и удалить контейнеры, а также удалить volumes с данными, выполните:

```bash
docker compose -f docker-compose.local.yml --env-file=.env.local  down -v
```

### 3. Организация тестирования базы данных

Тестирование базы данных в проекте организовано с использованием библиотеки `pytest` и `SQLAlchemy`. Тесты проверяют корректность подключения к базе данных, а также выполнение SQL-запросов и наличие ожидаемых данных в таблицах.

#### Структура пакета с тестами:

- conftest.py: Содержит фикстуры для создания подключения к базе данных и управления сессиями SQLAlchemy.
- test_database.py: Содержит тесты, которые проверяют подключение к базе данных и выполнение SQL-запросов.
- config.py: Содержит класс Settings, который загружает конфигурацию для подключения к базе данных из переменных окружения или файла .env.

#### Зависимости для тестирования

Для тестирования базы данных используются следующие зависимости:
- pytest: для написания и запуска тестов.
- SQLAlchemy: для работы с базой данных.
- psycopg2-binary: драйвер для подключения к PostgreSQL.

Зависимости указаны в конфигурационном файле pyproject.toml и устанавливаются автоматически при выполнении команды poetry install.

#### Запуск тестов

Перед запуском тестов убедитесь, что Docker-контейнер с PostgreSQL запущен.

Перед первым запуском тестов:
1. Создайте и активируйте виртуальное окружение
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Установите и настройте Poetry для создания виртуальных окружений в проекте
    ```bash
    pip install poetry
    poetry config virtualenvs.in-project true
    ```
3. Установите зависимости проекта:
    ```bash
    poetry install
    ```

Запустить тесты можно с помощью команды:
    ```bash
    poetry run pytest -v
    ```