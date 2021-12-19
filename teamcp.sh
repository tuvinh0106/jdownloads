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

LOGFILE="/root/logs/fclone.log"
FROM="gc:{0AHkNV_kj0aF9Uk9PVA}"
TO="gc:{0AJbitfhtYJSIUk9PVA}"

# CHECK FOR FILES IN FROM FOLDER THAT ARE OLDER THAN 15 MINUTES
#if find $FROM* -type f -mmin +1 | read
#  then
  start=$(date +'%s')
  echo "$(date "+%d.%m.%Y %T") FCLONE COPY STARTED" | tee -a $LOGFILE
  # MOVE FILES OLDER THAN 10 MINUTES 
  fclone copy "$FROM" "$TO" --drive-server-side-across-configs --stats=1s --stats-one-line -vP --checkers=500 --transfers=500 --drive-pacer-min-sleep=1ms --drive-pacer-burst=5000 --drive-stop-on-upload-limit --ignore-existing --ignore-checksum --check-first --log-file=$LOGFILE
  echo "$(date "+%d.%m.%Y %T") FCLONE COPY FINISHED IN $(($(date +'%s') - $start)) SECONDS" | tee -a $LOGFILE
#fi
exit
