# lab06
Пайплайн к 5 лабороторной работе


Краткий план, того что нужно сделать, чтобы протестировать пайплайн:
1) Создать пользователя в clickhouse;
2) Создать базу данных clickhouse_database;
3) Там создать таблицу "raw_clickstream" на основе данных из репозитория; 
4) Вставить данные;
5) Создать пользователя airflow;

По умолчанию используются такие параметры:

* airflow:    localhost:8080; Задаётся любой
* postgres:   localhost:5432; ***username***: airflow; ***password***: airflow
* redis:      localhost:6379;
* clickhouse: localhost:9000(8123); ***username***: clickhouse; ***password***: clickhouse; ***database***:clickhouse

Задать пользователя clickhouse/airflow можно через контейнер

Задаём пользователя clickhouse:
```
cd lab05/airflow
```
Для начала скопировать users.xml из контейнера и изменить
```
sudo docker cp clickhouse-server:/etc/clickhouse-server/users.xml /YOUR_PATH(Куда копируется файл)
```
```
nano /YOUR_PATH/users.xml
```
Найти параметр: <access_management>1</access_management>. Сделать его исполняемым.
Под ним должны быть установлены эти параметры, если их нет, то вставить.
* <named_collection_control>1</named_collection_control>
* <show_named_collections>1</show_named_collections>
* <show_named_collections_secrets>1</show_named_collections_secrets>
```
sudo docker cp /YOUR_PATH/users.xml clickhouse-server:/etc/clickhouse-server/users.xml
```
```
sudo docker compose exec clickhouse-server clickhouse-client
```
Задаем роль админа:
```
CREATE ROLE 'admin';
GRANT ALL ON *.* TO admin WITH GRANT OPTION;
```
Создаем пользователя clickhouse с паролем clickhouse (Используются в даге для подключения к базе).
```
create user clickhouse identified with plaintext_password by 'clickhouse';
GRANT admin to clickhouse;
```
Создаем бд
```
CREATE DATABASE clickhouse;
```
Создаем таблицу для семпла данных
```
CREATE TABLE clickhouse.raw_clickstream
(userId String,
 itemId String,
 action String,
 timestamp Float64
)
ENGINE = MergeTree()
ORDER BY timestamp;
```
Выходим из контейнера.
Вставляем данные в рабочий контейнер:
```
sudo docker compose exec -T clickhouse-server clickhouse-client --host localhost --port 9000 --user clickhouse --password clickhouse --query "INSERT INTO clickhouse.raw_clickstream FORMAT JSONEachRow" < our_dataset.jsonl
```
Пользователь в airflow задается через запущенный контейнер.
```
sudo docker compose exec airflow-webserver bash
```
```
airflow users create -u admin -f Ad -l Min -r Admin -e admin@adm.in
```
Пользователь от базы метаданных airflow задается по дефолту в Dockerfile.
