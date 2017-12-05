#!/bin/sh
if [ `id -u` -eq 0 ]; then
	echo "You must be root or use sudo to run this script."
	exit 1
fi

echo "***********************"
echo "* Creating GAUSS user *"
echo "***********************"
useradd -rU gauss

echo "****************************"
echo "* Installing prerequisites *"
echo "****************************"
apt-get -y install ffmpeg libnl-route-3-200
wget -O /tmp/gauss-hostapd.deb 'https://github.com/WSUGreenArrow/hostapd/releases/download/1.0_ga/hostapd-realtek_1.0_armhf.deb'
dpkg -i /tmp/gauss-hostapd.deb
rm /tmp/gauss-hostapd.deb

echo "*******************************"
echo "* Installing streaming script *"
echo "*******************************"
install -Dm 755 -T stream.py /usr/local/bin/gauss-stream

echo "**********************************"
echo "* Installing configuration files *"
echo "**********************************"
install -Dbm 644 conf/dnsmasq/gauss-wlan1.conf /etc/dnsmasq.d/
install -Dbm 644 conf/systemd/gauss.service /etc/systemd/system/
install -Dbm 644 conf/hostapd/hostapd.conf /etc/hostapd/
install -Dbm 644 conf/networking/gauss-wlan1.conf /etc/network/interfaces.d

# Modify dhcpcd to let wlan1 go
cat >> /etc/dhcpcd.conf <<END
# GAUSS
interface wlan1
static ip_address=10.107.101.1/24
END

echo "*********************"
echo "* Starting services *"
echo "*********************"
systemctl enable hostapd
systemctl start hostapd

systemctl enable gauss
systemctl start gauss

echo "*********"
echo "* Done! *"
echo "*********"
