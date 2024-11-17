CREATE DATABASE clickhouse;

CREATE TABLE clickhouse.raw_clickstream
(userId String,
 itemId String,
 action String,
 timestamp Float64
)
ENGINE = MergeTree()
ORDER BY timestamp;

INSERT INTO clickhouse.raw_clickstream 
FORMAT JSONEachRow
FROM 'docker-entrypoint-initdb.d/our_dataset.jsonl';
