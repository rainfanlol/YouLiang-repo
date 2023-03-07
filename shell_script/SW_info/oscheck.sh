#!/bin/bash
OS="cat /etc/redhat-release"
localip=172.16.110.39

echo "此OS版本是:"`$OS`

if [[ `$OS` =~ 6.7 ]];then


	if [[ `service snmpd status` =~ stop ]] ;then
	
	echo "SNMP沒啟動"
	
	service snmpd start
	chkconfig snmpd on

	elif [[ `service snmpd status` =~ running ]];then
	
        echo "SNMP啟動中"
        chkconfig snmpd on

	else
        echo "SNMP未安裝"
	mkdir /root/LinSNMPservice
	scp -r $localip:/root/LinSNMPservice/packages/package6.7 /root/LinSNMPservice/
	cd /root/LinSNMPservice/package6.7
	yum -y localinstall *.rpm
	service snmpd start
	chkconfig snmpd on
	fi


 #開通防火牆161/162 port並儲存設定重啟



	if [[ `service iptables status` =~ not ]];then
	echo "防火牆未開啟"
	else
	echo "防火牆開啟中加入port 161&162條件"
	iptables -I INPUT -p udp --dport 161 -j ACCEPT
	iptables -I INPUT -p udp --dport 162 -j ACCEPT
	/etc/rc.d/init.d/iptables save
	iptables-save > /etc/sysconfig/iptables
	service iptables save
	/etc/init.d/iptables restart
	fi
	

elif [[ `$OS` =~ 7.7 ]];then


	if [[ `systemctl status snmpd` =~ running ]];then
	echo "snmp功能啟動中"
	
	elif [[ `systemctl status snmpd` =~ dead ]];then
	echo "snmp功能目前未開啟幫您開啟"
	service snmpd start
	echo "snmp功能已開啟"
	systemctl enable snmpd.service
	
	else
	echo "snmp未安裝"
	mkdir /root/LinSNMPservice
	scp -r $localip:/root/LinSNMPservice/packages/package7.7 /root/LinSNMPservice/
	cd /root/LinSNMPservice/package7.7
	yum -y localinstall *.rpm
	service snmpd start
	systemctl enable snmpd.service
	echo "snmp安裝完並開啟"
	fi


 #以下開通防火牆161/162 port

#fire7.7=`systemctl status firewalld|grep 'Active'|awk '{print $2 $3}'`

	if [[ `systemctl status firewalld` =~ dead ]];then	
	echo "防火牆未開啟"

	else
	echo "防火牆開啟中加入port161&162條件"
	firewall-cmd --add-port=161/udp --permanent
	firewall-cmd --add-port=162/udp --permanent
	firewall-cmd --reload
	systemctl enable firewalld
	fi

else

echo "**************"
echo `$OS` "此版本不支援安裝"
echo "**************"


fi
