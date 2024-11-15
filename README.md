# lab06
Пайплайн к 5 лабороторной работе


Для того чтобы протестировать этот пайплайн нужно скачать файл 'raw_clickstream' из репозитория, распаковать его и вставить в clickhouse.

Создать базу данных clickhouse_database.
Там создать таблицу "raw_clickstream" на основе данных из репозитория. 

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

Создаем пользователя clickhouse с паролем clickhouse (Используются в даге для подключения к базе).

create user clickhouse identified with plaintext_password by 'clickhouse';
GRANT admin to clickhouse;

Проверялось на версии докера version 24.0.5

Пользователь в airflow задается через запущенный контейнер.

docker compose exec airflow-webserver bash

Пользователь от базы метаданных airflow задается по дефолту.

Clickhouse user: admin; password: admin
database: admin_database

Порт airflow: 8080
Порт postgres: 5432
Порт redis: 6379
