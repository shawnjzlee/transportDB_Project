tail -n +2 $1 | split -l $2 - split_
for file in split_*
do
	head -n 1 trip_data_1.csv > tmp_file
	cat $file >> tmp_file
	mv -f tmp_file $file
done
