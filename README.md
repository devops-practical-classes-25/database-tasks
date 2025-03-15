# dbms-tasks
Тренировочные задания для работы с СУБД

## Инструкция по запуску
### 1. Скачивание демонстрационной базы данных
Для скачивания и распаковки демонстрационной базы данных выполните следующие команды:

```bash
# Дайте права на выполнение скрипта
chmod +x load-demo-data.sh

Этот скрипт:
- Скачивает архив demo-small-en.zip с демонстрационной базой данных.
- Распаковывает его в каталог init/sql/.

# Запустите скрипт для скачивания и распаковки данных
./load-demo-data.sh
```

### 2. Запуск PostgreSQL и pgAdmin в Docker-контейнерах
Для запуска PostgreSQL и pgAdmin используйте Docker Compose. Убедитесь, что у вас установлены Docker и Docker Compose.

1. Убедитесь, что в корне проекта присутствует и заполнен файл .env.local.
2. Убедитесь, что порты 5433 и 5434 свободны на вашем компьютере.
3. Запустите контейнеры:

```bash
docker compose -f docker-compose.local.yml --env-file=.env.local  up -d
```

Это команда:
- Запускает контейнеры PostgreSQL и pgAdmin.
- При первом запуске контейнера с PostgreSQL применяется SQL-скрипт demo-small-en-20170815.sql для инициализации базы данных.

После запуска:
- PostgreSQL будет доступен на localhost:5433.
- pgAdmin будет доступен на localhost:5434.
- Подключитесь к PostgreSQL через pgAdmin, используя:
    * Host: postgres
    * Port: 5432
    * Username: postgres
    * Password: postgres
    * Database: postgres

### 3. Остановка контейнеров
Чтобы остановить и удалить контейнеры, выполните:

```bash
docker compose -f docker-compose.local.yml --env-file=.env.local  down -v
```

Чтобы остановить и удалить контейнеры, а также удалить volumes с данными, выполните:

```bash
docker compose -f docker-compose.local.yml --env-file=.env.local  down -v
```
