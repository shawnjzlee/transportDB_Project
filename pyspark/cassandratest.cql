CREATE KEYSPACE test_cassandra WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor' : 3};
CREATE TABLE test_cassandra.test (
  first varchar PRIMARY KEY,
  last varchar,
  hobby varchar
);
INSERT INTO test_cassandra.test (first, last, hobby) values ('Yogi', 'Berra', 'Baseball');
INSERT INTO test_cassandra.test (first, last, hobby) values ('Jack', 'London', 'Writing');
INSERT INTO test_cassandra.test (first, last, hobby) values ('Ada', 'Lovelace', 'Mechanical Computers');
INSERT INTO test_cassandra.test (first, last, hobby) values ('John', 'Glenn', 'Space Travel');
