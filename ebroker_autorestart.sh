#!/bin/bash
EBROKER_DATA_FOLDER="/home/sunnyyan/marketdata_cash/ebroker/data/parsed/hk_stock_0/"
EBROKER_STOP_SCT="/home/sunnyyan/marketdata_cash/ebroker/bin/stop_ebroker_connections.sh"
EBROKER_START_SCT="/home/sunnyyan/marketdata_cash/ebroker/bin/cron_start_ebroker_connections.sh"

MRNG_OPEN=930
MRNG_CLOSE=1200
AFTN_OPEN=1300
AFTN_CLOSE=1600
SLEEPINTERVAL=5

restart_ebroker() {
    CURHM=$1
    if [[ $CURHM -gt $MRNG_OPEN && $CURHM -lt $MRNG_CLOSE ]]
    then
        $EBROKER_STOP_SCT
        sleep 2
        $EBROKER_START_SCT
        sleep 3
    elif [[ $CURHM -gt $AFTN_OPEN && $CURHM -lt $AFTN_CLOSE ]]
    then
        $EBROKER_STOP_SCT
        sleep 2
        $EBROKER_START_SCT
        sleep 3
    fi
}

while [ 1 ]
do
    CURTIME=$(date +"%Y%m%d_%H%M%S")
    CURUNIXTIME=$(date +"%s")
    TODAY=$(date +"%Y%m%d")
    CURHM=$(date +"%-H%M")

    COUNT_EBROKER_PROCESS=$(ps aux | grep ebroker_connector | grep -v grep | wc -l)

    ################################################
    # check if the process for ebroker is running
    ################################################
    if [[ $COUNT_EBROKER_PROCESS -eq 0 ]]
    then
        restart_ebroker $CURHM
    fi
    ################################################
    # check if the file has become stale
    ################################################
    if [[ -e $EBROKER_DATA_FOLDER/$TODAY".csv" ]]
    then
        if [[ $(expr $CURUNIXTIME - $(date -r $EBROKER_DATA_FOLDER/$TODAY".csv" +"%s")) -gt 120 ]]
        then
            restart_ebroker $CURHM
        fi
    else
        restart_ebroker $CURHM
    fi
    ################################################
    # Exit if after trading hour
    ################################################
    if [[ $CURHM -gt $AFTN_CLOSE ]]
    then
        exit
    fi

    sleep $SLEEPINTERVAL
done
