CREATE KEYSPACE tripData WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor' : 3};

CREATE TABLE tripData.rides (
  medallion varchar,
  pickup_date timeuuid,
  pickup_time timeuuid,
  passenger_count float,
  pickup_long decimal,
  pickup_lat decimal,
  dropoff_long decimal,
  dropoff_lat decimal,
  PRIMARY KEY (pickup_date, pickup_time)
) WITH CLUSTERING ORDER BY (pickup_time DESC);
