CREATE KEYSPACE tripData WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor' : 3};

CREATE TABLE tripData.rides (
  medallion varchar PRIMARY KEY,
  pickup_date date,
  pickup_time time,
  passenger_count float,
  pickup_long decimal,
  pickup_lat decimal,
  dropoff_long decimal,
  dropoff_lat decimal
);
