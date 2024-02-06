#!/bin/bash
# GCLONE UPLOAD CRON TAB SCRIPT 
# chmod a+x /home/plex/scripts/rclone-upload.sh
# Type crontab -e and add line below (without #) and with correct path to the script
# * * * * * /home/plex/scripts/rclone-upload.sh >/dev/null 2>&1
# if you use custom config path add line bellow in line 20 after --log-file=$LOGFILE 
# --config=/path/rclone.conf (config file location)

if pidof -o %PPID -x "$0"; then
   exit 1
fi

array[0]="kullskill01"
array[1]="kullskill02"
array[2]="kullskill03"
array[3]="kullskill04"
array[4]="kullskill05"
array[5]="kullskill06"
array[6]="kullwill01"
array[7]="kullwill02"
array[8]="kullwill05"
array[9]="kullwill06"
array[10]="kullwill0708"
array[11]="kullwill09"
array[12]="kullwill10"
array[13]="kullwill14"
array[14]="kullwill15"
array[15]="kullwill16"



size=${#array[@]}
index=$(($RANDOM % $size))
echo ${array[$index]}

LOGFILE="/root/logs/gclone-upload.log"
FROM="/root/1Downloads/"
TO="${array[$index]}:{0AJT6R230-hUTUk9PVA}"

echo $TO

# CHECK FOR FILES IN FROM FOLDER THAT ARE OLDER THAN 15 MINUTES
if find $FROM* -type f -mmin +1 | read
  then
  start=$(date +'%s')
  echo "$(date "+%d.%m.%Y %T") GCLONE UPLOAD STARTED" | tee -a $LOGFILE
  # MOVE FILES OLDER THAN 10 MINUTES 
  gclone move "$FROM" "$TO" --filter "- *.part" --transfers=5 --checkers=5 --delete-after --min-age 1m --log-file=$LOGFILE --ignore-existing --ignore-checksum --drive-stop-on-upload-limit
  echo "$(date "+%d.%m.%Y %T") GCLONE UPLOAD FINISHED IN $(($(date +'%s') - $start)) SECONDS" | tee -a $LOGFILE
fi
exit

