#/bin/bash

if [[ $# -ne 2 ]]
then
    echo "Usage: arg 1 = Alert Level"
    echo "       arg 2 = Email Recipients"
    exit
fi

EMAIL_RECIPIENTS=$2
ALERT_LEVEL=$1
 
function check_and_mail() {
 
  while read output;
 
  do
 
    partition=$(echo $output | awk '{ print $1 }')
    percentage=$(echo $output | awk '{ print $2 }' | cut -d"%" -f1)
    mounted_on=$(echo $output | awk '{ print $3 }')
 
    if [ $percentage -ge $ALERT_LEVEL ] ; then
      echo "$partition (mounted on $mounted_on): $percentage%" | mail -s "Disk Space is running out of space: $percentage%" $EMAIL_RECIPIENTS
    fi
 
  done
 
}
 
df -hP | grep -vE "^Filesystem|tmpfs|cdrom" | awk '{ print $1 " " $5 " " $6 }' | check_and_mail
