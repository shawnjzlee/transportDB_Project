CREATE KEYSPACE tripData WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor' : 3};

CREATE TABLE tripData.rides (
  medallion varchar PRIMARY KEY,
  pickup_datetime varchar PRIMARY KEY,
  passenger_count float,
  pickup_long float,
  pickup_lat float,
  dropoff_long float,
  dropoff_lat float
);
