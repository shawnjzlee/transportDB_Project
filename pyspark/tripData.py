from __future__ import print_function

import sys

from datetime import datetime
from pyspark.sql import SQLContext 
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql.types import * 
from pyspark.sql.functions import col, udf, unix_timestamp
from pyspark_cassandra import CassandraSparkContext 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: tripData.py <file>", file=sys.stderr)
        exit(-1)

    conf = SparkConf().setAppName("Taxi Data")
    sc = CassandraSparkContext(conf=conf) 
    sqlContext = SQLContext(sc)

    customSchema = StructType([ \
            StructField("medallion", StringType(), True), \
            StructField("hack_license", StringType(), True), \
            StructField("vendor_id", StringType(), True), \
            StructField("rate_code", StringType(), True), \
            StructField("store_and_fwd_flag", StringType(), True), \
            StructField("pickup_datetime", TimestampType(), True), \
            StructField("dropoff_datetime", TimestampType(), True), \
            StructField("passenger_count", FloatType(), True), \
            StructField("trip_time_in_secs", FloatType(), True), \
            StructField("trip_distance", FloatType(), True), \
            StructField("pickup_longitude", DecimalType(), True), \
            StructField("pickup_latitude", DecimalType(), True), \
            StructField("dropoff_longitude", DecimalType(), True), \
            StructField("dropoff_latitude", DecimalType(), True)])

    rides = sqlContext.read.format('com.databricks.spark.csv') \
                .options(header='true') \
                .load(sys.argv[1], schema=customSchema)
                
    temp = rides.map(lambda row: {   'medallion': row.medallion,
                                        'pickup_datetime': row.pickup_datetime,
                                        'passenger_count': row.passenger_count,
                                        'pickup_long': row.pickup_longitude,
                                        'pickup_lat': row.pickup_latitude,
                                        'dropoff_long': row.dropoff_longitude,
                                        'dropoff_lat': row.dropoff_latitude}).collect() 

    # from_pattern = 'yyyy-MM-dd hh:mm:ss' # 2013-01-01 15:11:48
    # to_date_pattern = 'yyyy-MM-dd'
    # to_time_pattern = 'hh:mm:ss'
    
    # temp2 = temp.withColumn('pickup_datetime')
    
    # temp.withColumn('pickup_datetime', from_unixtime(unix_timestamp(df['date'], from_pattern), to_date_pattern)).show()
    # temp.withColumn('pickup_time', from_unixtime(unix_timestamp(df[''])) )

    sc.parallelize(temp).saveToCassandra(keyspace='tripdata', table='rides')
