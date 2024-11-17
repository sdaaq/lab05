# lab06

Чтобы запустить сборку, нужно перейти в корень репозитория и ввести в bash:
```
sudo docker compose -f docker-compose.yml up
```


## Пайплайн к 5 лабораторной работе

По умолчанию используются такие параметры:

* airflow:    localhost:8080; ***username***: admin; ***password***: admin
* postgres:   localhost:5432; ***username***: airflow; ***password***: airflow
* redis:      localhost:6379;
* clickhouse: localhost:9000(8123); ***username***: clickhouse; ***password***: clickhouse; ***database***:clickhouse


Секретные параметры для workflow задаются в настройках github. 
Secrets and vars.
* "username: ${{ secrets.DOCKER_USERNAME }}"
* "password: ${{ secrets.DOCKER_PASSWORD }}"
