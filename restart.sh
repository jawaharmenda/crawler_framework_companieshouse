#!/bin/bash
home_dir="/home/jawahar/chcrawl"
numoffiles=$(ls -f $home_dir/output/|wc -l)
echo $numoffiles
expectedfiles=$(wc -l $home_dir/ch_url.txt|awk '{print $1}')
echo $expectedfiles

while [[ $expectedfiles -gt $numoffiles ]]; do
	numoffiles=$(ls -f $home_dir/output/|wc -l)
	echo "total files crawled till now are "$numoffiles
	#statements
	pid=$(ps -ef | grep python3 | grep -v "grep" | wc -l)
	#echo $pid
	if [[ $pid -eq 0 ]]; then
		echo "No running process found .Restarting"
		nohup python3 $home_dir/comphouse.py $home_dir/ch_url.txt $home_dir/output/ &
		sleep 60
	fi
sleep 60
done
echo "done"
