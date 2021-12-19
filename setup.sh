#!/usr/bin/env bash

cd
echo "-----> Install gclone"
wget https://dl.dropboxusercontent.com/s/py5datuvmrhj3a8/gclone
mv gclone /usr/bin/
chmod +x /usr/bin/gclone
echo "-----> Gclone Installed"

echo "-----> Download SA"
wget https://raw.githubusercontent.com/tuvinh0106/jdownloads/main/admin.zip
wget https://raw.githubusercontent.com/tuvinh0106/jdownloads/main/admin2.zip
wget https://raw.githubusercontent.com/tuvinh0106/jdownloads/main/adm3.zip
unzip -o accounts.zip
rm accounts.zip
echo "-----> SA Downloaded"

echo "-----> Download Gclone Config"
cd ~
mkdir -p /root/.config/rclone/
wget "https://raw.githubusercontent.com/tuvinh0106/jdownloads/main/rclone.conf" -O /root/.config/rclone/rclone.conf
echo "-----> Gclone Config successfully"

echo "-----> Install Tmux"
apt install tmux
echo "-----> Tmux installed successfully"
gclone --version
echo "----> Install Crontab, Auto move File"
apt install cron -y
apt install nano -y
apt install nload -y
apt install htop -y
apt install zip -y
mkdir /root/logs
touch /root/logs/gclone-upload.log
wget https://raw.githubusercontent.com/tuvinh0106/jdownloads/main/teamcp.sh
chmod a+x teamcp.sh
wget https://raw.githubusercontent.com/tuvinh0106/jdownloads/main/rclone-upload.sh
chmod a+x rclone-upload.sh
crontab -l | { cat; echo "* * * * * /root/rclone-upload.sh >/dev/null 2>&1"; } | crontab -
/etc/init.d/cron start
/etc/init.d/cron status
echo "------> Crontab configured successfully"
