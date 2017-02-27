cqlsh -f tripData.cql spark13
spark-submit --master spark://spark13.cs.ucr.edu:7077 --packages TargetHolding:pyspark-cassandra:0.3.5,com.databricks:spark-csv_2.11:1.5.0 --conf spark.cassandra.connection.host=spark13 $@
