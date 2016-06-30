#!/bin/bash
CURTIME=$(date +"%Y%m%d_%H%M%S_000000")
TODAY=$(date +"%Y%m%d")

for i in $(cat ~/usefulscripts/instrumentlist.txt)
do
    echo $CURTIME,subscription,HKSE,$i,$TODAY,$TODAY | nc localhost 11010
    sleep 0.3
done

for i in $(cat ~/usefulscripts/instrumentlist_orc.txt)
do
    echo $CURTIME,subscription,HKSE,$i,$TODAY,$TODAY | nc localhost 12010
    sleep 0.3
done
