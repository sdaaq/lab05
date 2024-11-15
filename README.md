# lab06
Пайплайн к 5 лабороторной работе


Для того чтобы протестировать этот пайплайн нужно скачать файл 'raw_clickstream' из репозитория, распаковать его и вставить в clickhouse.

Создать базу данных clickhouse_database.
Там создать таблицу "raw_clickstream" на основе данных из репозитория. 
Вставить данные.
По умолчанию используются такие параметры:
airflow:    localhost:8080; Задаётся любой
postgres:   localhost:5432; username: airflow; password: airflow
redis:      localhost:6379;
clickhouse: localhost:9000(8123); Задаётся username: clickhouse; password: clickhouse; database:clickhouse
Задать пользователя можно через контейнер
sudo docker compose exec clickhouse-server clickhouse client

По умолчанию установлен пользователь default.
Нужно создать пользователя clickhouse с паролем clickhouse
Для начала скопировать users.xml из контейнера и изменить
sudo docker cp clickhouse-server:/etc/clickhouse-server/users.xml /tmp
Файл может лежать во внутренних tmp докера.
cd /tmp
nano users.xml

Сделать видимым параметр <access_management>1</access_management>

docker cp /YOUR_PATH/users.xml clickhouse-server:/etc/clickhouse-server/users.xml

sudo docker compose exec clickhouse-server clickhouse-client
Задаем роль админа:
CREATE ROLE 'admin';
GRANT ALL ON *.* TO admin WITH GRANT OPTION;

Создаем бд
CREATE DATABASE clickhouse;

Создаем таблицу для семпла данных

CREATE TABLE clickhouse.raw_clickstream
(userId String,
 itemId String,
 action String,
 timestamp Float64
)
ENGINE = MergeTree()
ORDER BY timestamp;

Создаем пользователя clickhouse с паролем clickhouse (Используются в даге для подключения к базе).

create user clickhouse identified with plaintext_password by 'clickhouse';
GRANT admin to clickhouse;

Проверялось на версии докера version 24.0.5

Пользователь в airflow задается через запущенный контейнер.

docker compose exec airflow-webserver bash

Пользователь от базы метаданных airflow задается по дефолту.

Clickhouse user: admin; password: admin
database: admin_database
