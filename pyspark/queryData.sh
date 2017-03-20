#!/bin/bash
day=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
for ((i = 0; i < $1; i++))
do
	starting_hour=(00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23)
	ending_hour=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24)
	for j in {0..23}
	do
		#let ending_hour=$((10#$starting_hour + 1))
		echo "select pickup_lat,pickup_long from tripdata.rides where pickup_date = '2013-"$2"-"${day[i]}"' and pickup_time < '"${ending_hour[j]}":00:00' and pickup_time > '"${starting_hour[j]}":00:00' LIMIT 175000;" > query.cql
		cqlsh -f query.cql spark13 >> location"${day[i]}".txt
		#echo "location"${day[i]}".txt"
		#echo "2013-01-"${day[i]} ${starting_hour[j]} ${ending_hour[j]}
	done
done


# $1 refers to the date you want
# $2 refers to later time in time range
# $3 refers to earlier time in time range
# $4 refers to the name of the .txt's that you'll be making
