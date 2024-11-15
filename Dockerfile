FROM python:3.8.13

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --user psycopg2-binary==2.9.9 && \
    pip install 'apache-airflow[postgres]==2.9.2' \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.2/constraints-3.8.txt" && \
    pip install redis && \
    pip install clickhouse-connect && \
    pip install clickhouse-driver

WORKDIR /home/ubuntu/lab05/airflow
ENV AIRFLOW_HOME=/home/ubuntu/lab05/airflow
ENV PATH=/root/.local/bin:$PATH

# меняем тип эксзекутора для Airflow на LocalExecutor (запускает задачи параллельно, но только на одной машине)
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
# указываем подключение к постгре
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
# отключаем загрузку примеров дагов
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
# отключаем загрузку соединений по умолчанию
ENV AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False
# и еще два флажка, полезных при отладке
# отображать имя хоста в логах
ENV AIRFLOW__CORE__EXPOSE_HOSTNAME=True
# отображать трассировку стека при возникновении ошибки
ENV AIRFLOW__CORE__EXPOSE_STACKTRACE=True
# секретный ключ
ENV AIRFLOW__WEBSERVER__SECRET_KEY=abc




