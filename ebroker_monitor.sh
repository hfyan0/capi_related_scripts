#!/bin/bash
TMP_FILE=/tmp/monitor_ebroker
#EBROKER_DATA_FOLDER="/home/cashadmin/marketdata/ebroker/data/parsed/hsi_hhi_future/"
EBROKER_DATA_FOLDER="/home/smartwise/marketdata/ebroker/data/parsed/smartwise_hk_stock/"

MRNG_OPEN=930
MRNG_CLOSE=1200
AFTN_OPEN=1300
AFTN_CLOSE=1600

while [ 1 ]
do
    CURTIME=$(date +"%Y%m%d_%H%M%S")
    CURUNIXTIME=$(date +"%s")
    TODAY=$(date +"%Y%m%d")

    COUNT_EBROKER=$(ps aux | grep ebroker_connector | grep -v grep | wc -l)

    ################################################
    if [[ $COUNT_EBROKER -eq 0 ]]
    then
        echo "ebroker down. Please check." > $TMP_FILE
        /sbin/ifconfig -a >> $TMP_FILE
        NEED_SEND_ALERT=0
        if [[ $(date +'%H%M') -gt $MRNG_OPEN && $(date +'%H%M') -gt $MRNG_CLOSE ]]; then NEED_SEND_ALERT=0; fi
        if [[ $(date +'%H%M') -gt $AFTN_OPEN && $(date +'%H%M') -gt $AFTN_CLOSE ]]; then NEED_SEND_ALERT=1; fi

        if [[ $NEED_SEND_ALERT -eq 1 ]]
        then
            cat $TMP_FILE | mail -s "[Urgent] ebroker was down as at $TODAY $CURTIME." sunny.yan@cashalgo.com
        fi
    fi
    ################################################
    if [[ -e $EBROKER_DATA_FOLDER/$TODAY".csv" ]]
    then
        if [[ $(expr $CURUNIXTIME - $(date -r $EBROKER_DATA_FOLDER/$TODAY".csv" +"%s")) -gt 120 ]]
        then
            echo "Market data stale. Please check." > $TMP_FILE
            /sbin/ifconfig -a >> $TMP_FILE

            NEED_SEND_ALERT=0
            if [[ $(date +'%H%M') -gt $MRNG_OPEN && $(date +'%H%M') -gt $MRNG_CLOSE ]]; then NEED_SEND_ALERT=0; fi
            if [[ $(date +'%H%M') -gt $AFTN_OPEN && $(date +'%H%M') -gt $AFTN_CLOSE ]]; then NEED_SEND_ALERT=1; fi

            if [[ $NEED_SEND_ALERT -eq 1 ]]
            then
                cat $TMP_FILE | mail -s "[Urgent] ebroker market data stale as at $TODAY $CURTIME." sunny.yan@cashalgo.com
            fi
        fi
    else
        echo "ebroker market data file not exist. Please check." > $TMP_FILE
        /sbin/ifconfig -a >> $TMP_FILE

        NEED_SEND_ALERT=0
        if [[ $(date +'%H%M') -gt $MRNG_OPEN && $(date +'%H%M') -gt $MRNG_CLOSE ]]; then NEED_SEND_ALERT=0; fi
        if [[ $(date +'%H%M') -gt $AFTN_OPEN && $(date +'%H%M') -gt $AFTN_CLOSE ]]; then NEED_SEND_ALERT=1; fi

        if [[ $NEED_SEND_ALERT -eq 1 ]]
        then
            cat $TMP_FILE | mail -s "[Urgent] ebroker market data file not exist as at $TODAY $CURTIME." sunny.yan@cashalgo.com
        fi
    fi
    ################################################

    sleep 60
done
