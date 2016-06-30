#/bin/bash

if [[ $# -ne 2 ]]
then
    echo "Usage: arg 1 = Folder containing riskfeeds"
    echo "       arg 2 = Email recipients"
    exit
fi

RISKFEED_FOLDER=$1
EMAIL_RECIPIENTS=$2
RISKFEED_TMPFILE=/tmp/chkriskfeed1.tmp
TMPFILE_EMAIL=/tmp/chkriskfeed2.tmp

NUM_OF_LINES=$(find $RISKFEED_FOLDER | grep riskfeed | grep csv | sort | xargs cat | wc -l)

while [ 1 ]
do

  find $RISKFEED_FOLDER | grep riskfeed | grep csv | sort | xargs cat > $RISKFEED_TMPFILE
  NEW_NUM_OF_LINES=$(cat $RISKFEED_TMPFILE | wc -l)

  if [[ $NEW_NUM_OF_LINES -gt $NUM_OF_LINES ]]
  then
    rm -f $TMPFILE_EMAIL
    echo "---START OF EMAIL------------------" >> $TMPFILE_EMAIL
    echo "This is automatically sent from the riskfeed checking script." >> $TMPFILE_EMAIL
    echo                                       >> $TMPFILE_EMAIL
    echo "-----------------------------------" >> $TMPFILE_EMAIL
    date +'%Y-%m-%d %H:%M:%S'                  >> $TMPFILE_EMAIL
    echo                                       >> $TMPFILE_EMAIL
    ifconfig                                   >> $TMPFILE_EMAIL
    echo                                       >> $TMPFILE_EMAIL
    echo "---Riskfeed folder:----------------" >> $TMPFILE_EMAIL
    echo $RISKFEED_FOLDER                      >> $TMPFILE_EMAIL
    echo                                       >> $TMPFILE_EMAIL
    echo "---List of files-------------------" >> $TMPFILE_EMAIL
    find $RISKFEED_FOLDER | grep csv$          >> $TMPFILE_EMAIL
    echo                                       >> $TMPFILE_EMAIL
    echo "---Riskfeeds-----------------------" >> $TMPFILE_EMAIL
    cat $RISKFEED_TMPFILE                      >> $TMPFILE_EMAIL
    echo                                       >> $TMPFILE_EMAIL
    echo "---END OF EMAIL--------------------" >> $TMPFILE_EMAIL

    cat $TMPFILE_EMAIL
    #cat $TMPFILE_EMAIL | mail -s "Riskfeed: Please check. "$(date +'%Y%m%d %H:%M:%S') $EMAIL_RECIPIENTS
    NUM_OF_LINES=$NEW_NUM_OF_LINES
  fi

  sleep 2
 
done
