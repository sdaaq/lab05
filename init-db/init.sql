CREATE ROLE 'admin';
GRANT ALL ON *.* TO admin WITH GRANT OPTION;

create user clickhouse identified with plaintext_password by 'clickhouse';
GRANT admin to clickhouse;

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
FROM INFILE '/docker-entrypoint-initdb.d/our_dataset.jsonl'
FORMAT JSONEachRow;
