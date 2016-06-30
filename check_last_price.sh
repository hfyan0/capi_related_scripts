#!/bin/bash

DATAFILE=/home/smartwise/marketdata/ebroker/data/parsed/smartwise_hk_stock/$(date +'%Y%m%d').csv
OUTPUTFILE=/home/smartwise/dailyLastPrice.txt
TMPFILE=/tmp/haha

rm -f $TMPFILE

for i in $(cat $DATAFILE | awk -F"," '{print $2}' | sort | uniq)
do
    cat $DATAFILE | grep ,$i, | tail -1 >> $TMPFILE
done

cat $TMPFILE | awk -F"," '{print $2,"\t",$3}' > $OUTPUTFILE
