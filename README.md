# lab06
Пайплайн к 5 лабороторной работе


Для того чтобы протестировать этот пайплайн нужно скачать файл 'raw_clickstream', распаковать его и вставить в clickhouse.

Создать базу данных clickhouse_database.
Там создать таблицу "raw_clickstream" на основе данных из репозитория. 

Задать пользователя можно через контейнер

Проверялось на версии докера version 24.0.5
ip:port для подключения к кликхаусу и редису задаются в python скрипте

Пользователь в airflow задается через запущенный контейнер с помощью команды docker compose exec airflow-webserver bash
Пользователь от базы метаданных airflow задается по дефолту.

Clickhouse user: admin; password: admin
database: admin_database

Порт airflow: 8080
Порт postgres: 5432
Порт redis: 6379
