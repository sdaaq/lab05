import csv
import clickhouse_driver
import redis

import psycopg2

from clickhouse_connect.driver.external import ExternalData
import clickhouse_connect

import contextlib


import pendulum
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context

DEFAULT_ARGS = {"owner": "newprolab"}
TREE_FILE_TEMPLATE = '/tmp/tmp_tree.csv'


@dag(
    default_args=DEFAULT_ARGS,
    schedule_interval="0 * * * *",
    start_date=pendulum.datetime(2020, 11, 20),
    catchup=True,
)
def lab05():
    @task
    def download_tree():
        context = get_current_context()
        tree_file = TREE_FILE_TEMPLATE
        with contextlib.closing(
                psycopg2.connect(
                    database="sku_info",
                    user="lab05",
                    password="zua0ieMahk9Jei",
                    host="data.ijklmn.xyz",
                    port="5433"
                )
        ) as conn:
            cur = conn.cursor()
            cur.execute("""WITH RECURSIVE tree(id, cat, parent_id, path) AS (
                            SELECT id, cat, parent_id, array[id]::integer[]
                            FROM category_tree WHERE cat BETWEEN 10 and 99
                            UNION ALL
                            SELECT category_tree.id, category_tree.cat, category_tree.parent_id, path || array[category_tree.id]::integer[]
                            FROM category_tree INNER JOIN tree on tree.id = category_tree.parent_id),
                     tmp as(SELECT tree.id, tree.cat, tree.parent_id, tree.path[1] as pa
                            FROM tree),
                     tmp_1 as(select MAX(id) as id_m, cat
                              from tmp
                              group by cat),
                     tmp_2 as (select id_m, cat, (select parent_id from tmp where id_m = id) as par_id, (select pa from tmp where id_m = id) as path
                               from tmp_1)
                     select tmp_2.*, (select cat from tmp where tmp_2.path = tmp.id) as category, sku_id
                     from tmp_2
                     inner join sku_cat using(cat);""")
            our_tree = cur.fetchall()
            with open(tree_file, 'w') as f_tree:
                tmp_writer = csv.writer(f_tree)
                tmp_writer.writerows(our_tree)
        return tree_file

    @task(retries=3)
    def aggregate_counts(tree_file_path, timeout=3600):
        client = clickhouse_connect.get_client(host='localhost', port=8123, username='clickhouse', \
                                               password='clickhouse', database='clickhouse')

        context = get_current_context()
        """2-Й ЭТАП: ЗАГРУЗКА ДЕРЕВА В CLICKHOUSE и расчет нужного ответа"""

        ext_data = ExternalData(file_path=tree_file_path,
                                fmt='CSV',
                                structure=['id_m UInt32', 'cat UInt32', 'par_id UInt32', 'path UInt32',
                                           'category UInt32', 'sku_id String'])
        s_year = context["logical_date"].year
        s_month = context["logical_date"].month
        s_day = context["logical_date"].day
        s_hour = context["logical_date"].hour

        result = client.query(f"""WITH TCE AS(SELECT itemId,
        	   timestamp,
        	   makeDateTime(YEAR(toTimezone(FROM_UNIXTIME(toUnixTimestamp(`timestamp`)), 'UTC')),
        	   				MONTH(toTimezone(FROM_UNIXTIME(toUnixTimestamp(`timestamp`)), 'UTC')),
        	   				DAY(toTimezone(FROM_UNIXTIME(toUnixTimestamp(`timestamp`)), 'UTC')),
        	   				HOUR(toTimezone(FROM_UNIXTIME(toUnixTimestamp(`timestamp`)), 'UTC')),
        	   				0, 0, 'UTC') AS date_hour
                            FROM clickhouse.raw_clickstream
                            WHERE action == 'favAdd'),
               TCE_1 AS(SELECT * 
        		        FROM TCE
        		        LEFT JOIN tmp_tree ON concat('sku:', tmp_tree.sku_id) == TCE.itemId),
               TCE_2 AS(SELECT MIN(timestamp), date_hour, category, COUNT(*) AS count_cat
        		        FROM TCE_1
        		        GROUP BY date_hour, category
        		        ORDER BY date_hour, COUNT(*) DESC, MIN(timestamp)),
               TCE_3 AS(SELECT TCE_2.*,
        	   	        ROW_NUMBER() OVER(PARTITION BY date_hour ORDER BY count_cat DESC) AS top
        	            FROM TCE_2),
               TCE_4 AS(SELECT date_hour, groupArray(category) AS gr_cat
        		        FROM TCE_3
        		        WHERE top < 6
        		        GROUP BY date_hour
        		        ORDER BY date_hour)
               SELECT concat('fav:level2:', toString(YEAR(date_hour)),
        			    '-', toString(MONTH(date_hour)),
        			    '-', toString(DAY(date_hour)),
        			    ':', IF(HOUR(date_hour) < 10, concat('0', toString(HOUR(date_hour))), toString(HOUR(date_hour))), 'h:top5') AS naming, gr_cat
               FROM TCE_4
	       WHERE HOUR(date_hour) == {s_hour} AND
                     MONTH(date_hour) == {s_month} AND
                     DAY(date_hour) == {s_day} AND
                     HOUR(date_hour) == {s_hour};""", external_data=ext_data)

        db = redis.Redis(host='localhost', port=6379)
        counter = 0
        for line in result.result_rows:
            counter += 1
            print(line[0], *list(line[1]))
            db.sadd(line[0], *list(line[1]))

    aggregate_counts(download_tree())


actual_dag = lab05()
