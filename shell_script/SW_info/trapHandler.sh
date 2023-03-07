#!/bin/bash
logfile='/etc/snmp/traps.txt'
testfile='/etc/icinga2/scripts/trap/test.txt'

read host
read ip
TODAY=`date +%Y/%m/%d\ %H:%M:%S`

IpHandle=`echo $ip |sed 's/]:/@/g' |sed "s/: \[/@/g" |awk -F "@" '{print $2}'`
###判斷trap來的ip是否在客戶清單,存在則會把訊息處理後存DB
DATABASE="icinga2"
TABLE="mirle_view_AllActiveHostsAddress"
mysql_query="select address from $TABLE WHERE ServiceType='Snmptrap'"
mysql_result=`sudo mysql -D ${DATABASE} -N -e "${mysql_query}"`
for ips in ${mysql_result[@]};do
 if [ $ips == $IpHandle ];then
  vars=
  while read oid val
  do
   if [ "$vars" = "" ]
   then
    vars="$oid = $val"
   else
    vars="$vars , $oid = $val"
   fi
  done

##查看使用者
#  whome=`sudo whoami`
#  echo $whome >> $testfile


  traptest=`echo $vars |sed 's/,/\n/g'`
#  traptest1=`echo $vars |sed 's/,/\\n/g'`
#  testu=`echo $vars |sed 's/.0//g' |sed -e 's/,/\\n/g'`
#  mail=echo $vars |sed 's/.0//g' |sed 's/,/\\n/g' |awk -F "::" '{print $2}'
  TrapResult=`echo $vars |sed 's/.0//g' |sed -e 's/,/\\\n/g'`
#  get_value=`echo $TrapResult |sed -e 's/\\n//\\\\n/g'`
  echo $TrapResult |sed -e 's/\\n/\\\\n/g' > $logfile
  get_value=`cat /etc/snmp/traps.txt`

  mysql_customLocation="select customLocation from mirle_view_AllActiveHostsAddress WHERE address='$IpHandle' and ServiceType='Snmptrap'"
  get_sql_customLocation=`sudo mysql -D icinga2 -N -e "${mysql_customLocation}"`
  customLocation=$get_sql_customLocation

  ServiceName="SNMP_Trap"
  Statu=`echo $vars |sed 's/.0//g' |sed "s/,/\\n/g" |awk -F "::" '{print $2}' |grep 'alertCurrentStatus' |awk -F "=" '{print $2}' |sed "s/ok/0/g" |sed "s/WARNING/1/g" |sed "s/CRITICAL/2/g" |sed "s/UNKNOWN/3/g"`
  db_insert_time=$TODAY
  output2=`echo $vars |sed 's/.0//g' |sed "s/,/\\n/g" |grep 'SNMPv2-MIB::snmpTrapOID' |awk -F "=" '{print $2}' |awk -F "::" '{print $2}'`
#  get_ipFrom="TrapTitle:"${output2}"___Location:"${customLocation}
  get_ipFrom=${output2}

  mysql_devicename="select display_name from mirle_view_AllActiveHostsAddress WHERE address='$IpHandle' and ServiceType='Snmptrap'"
  get_sql_devicename=`sudo mysql -D icinga2 -N -e "${mysql_devicename}"`
  get_HOSTNAME=$get_sql_devicename

  mysql_deviceType="select customDeviceType from mirle_view_AllActiveHostsAddress WHERE address='$IpHandle' and ServiceType='Snmptrap'"
  get_sql_deviceType=`sudo mysql -D icinga2 -N -e "${mysql_deviceType}"`
  deviceType=$get_sql_deviceType

  mysql_uniformNumber="select customUniformNumber from mirle_view_AllActiveHostsAddress WHERE address='$IpHandle' and ServiceType='Snmptrap'"
  get_sql_uniformNumber=`sudo mysql -D icinga2 -N -e "${mysql_uniformNumber}"`
  uniformNumber=$get_sql_uniformNumber

#trap訊息寫入db
  sqlQuery="INSERT INTO mirle_mon_Service_SnmpTrap(hostName,serviceName,recordedOn,state,output,longOutput,IP,deviceType,uniformNumber) VALUES ('${get_HOSTNAME}','${ServiceName}','${db_insert_time}','${Statu}','${get_ipFrom}','$get_value','${IpHandle}','${deviceType}','${uniformNumber}');"
  sudo mysql -D icinga2 -e "$sqlQuery"

##################################################


###發mail
  mailMessage=`echo $vars |sed 's/.0//g' |sed -e 's/,/\\n/g'`
##統編
  mysql_query="select customUniformNumber FROM mirle_view_AllActiveHostsAddress WHERE address='$IpHandle' and ServiceType='Snmptrap'"
  mysql_result=`sudo mysql -D icinga2 -N -e "${mysql_query}"`


  mysql_email="SELECT NotificationContacts FROM mirle_view_AllActiveHostsNotificationContacts WHERE ServiceType='Snmptrap' and Address='$IpHandle'"
  mysql_result2=`sudo mysql -D icinga2 -N -e "${mysql_email}"`
  mysql_result3=`echo $mysql_result2 |sed 's/;/ /g'`
#  mysql_result2=`sudo mysql -D icinga2 -N -e "${mysql_email}"`
#由db提供mail
  emaillist="$mysql_result3"

###ServiceDJ 聯絡人資訊
  mysql_CompanyName="SELECT Name FROM mirle_customer_info WHERE UniformSerialNumber ='$mysql_result'"
  customerInfo_CompanyName=`sudo mysql -D icinga2 -N -e "${mysql_CompanyName}"`
  mysql_CompanyAddress="SELECT Address FROM mirle_customer_info WHERE UniformSerialNumber ='$mysql_result'"
  customerInfo_CompanyAddress=`sudo mysql -D icinga2 -N -e "${mysql_CompanyAddress}"`
  mysql_CompanyPhoneNumber="SELECT PhoneNumber FROM mirle_customer_info WHERE UniformSerialNumber ='$mysql_result'"
  customerInfo_CompanyPhoneNumber=`sudo mysql -D icinga2 -N -e "${mysql_CompanyPhoneNumber}"`
  mysql_CompanyContactor="SELECT Contactor FROM mirle_customer_info WHERE UniformSerialNumber ='$mysql_result'"
  customerInfo_CompanyContactor=`sudo mysql -D icinga2 -N -e "${mysql_CompanyContactor}"`

###ServiceDJ 系統資訊
  mysql_DJ_version="SELECT version FROM mirle_msp_version ORDER BY Id DESC LIMIT 1;"
  ServiceDJ_version=`sudo mysql -D icinga2 -N -e "${mysql_DJ_version}"`

  mysql_ServiceDJ_HostErrorStatus="SELECT COUNT(*) AS HostErrorStatus FROM icinga_hoststatus 
  LEFT JOIN icinga_objects ON icinga_hoststatus.host_object_id = icinga_objects.object_id
  LEFT JOIN icinga_customvariables ON icinga_customvariables.object_id = icinga_objects.object_id
  WHERE icinga_objects.is_active = 1 AND icinga_hoststatus.current_state <> 0
  AND icinga_customvariables.varname = 'uniformNumber'
  AND icinga_customvariables.varvalue = \"${mysql_result}\";"
  ServiceDJ_HostErrorStatus=`sudo mysql -D icinga2 -N -e "${mysql_ServiceDJ_HostErrorStatus}"`

  mysql_ServiceDJ_HostsTotal="SELECT COUNT(*) AS HostsTotal FROM icinga_hosts
  LEFT JOIN icinga_objects ON icinga_hosts.host_object_id = icinga_objects.object_id
  LEFT JOIN icinga_customvariables ON icinga_customvariables.object_id = icinga_objects.object_id
  WHERE icinga_objects.is_active = 1 AND icinga_hosts.address IS NOT NULL
  AND icinga_customvariables.varname = 'uniformNumber'
  AND icinga_customvariables.varvalue = \"${mysql_result}\";"
  ServiceDJ_HostsTotal=`sudo mysql -D icinga2 -N -e "${mysql_ServiceDJ_HostsTotal}"`

  mysql_ServiceDJ_ServiceErrorStatus="SELECT COUNT(*) AS ServiceErrorStatus FROM icinga_servicestatus
  LEFT JOIN icinga_services ON icinga_servicestatus.service_object_id = icinga_services.service_object_id
  LEFT JOIN icinga_objects ON icinga_servicestatus.service_object_id = icinga_objects.object_id
  LEFT JOIN icinga_hosts ON icinga_hosts.host_object_id = icinga_services.host_object_id
  LEFT JOIN icinga_customvariables ON icinga_customvariables.object_id = icinga_hosts.host_object_id
  WHERE icinga_objects.is_active = 1 AND icinga_servicestatus.current_state <> 0
  AND icinga_customvariables.varname = 'uniformNumber'
  AND icinga_customvariables.varvalue = \"${mysql_result}\";"
  ServiceDJ_ServiceErrorStatus=`sudo mysql -D icinga2 -N -e "${mysql_ServiceDJ_ServiceErrorStatus}"`

  mysql_ServiceDJ_ServicesTotal="SELECT COUNT(*) AS ServicesTotal FROM icinga_services
  LEFT JOIN icinga_objects ON icinga_services.host_object_id = icinga_objects.object_id
  LEFT JOIN icinga_customvariables ON icinga_customvariables.object_id = icinga_objects.object_id
  WHERE icinga_objects.is_active = 1
  AND icinga_customvariables.varname = 'uniformNumber'
  AND icinga_customvariables.varvalue = \"${mysql_result}\";"
  ServiceDJ_ServicesTotal=`sudo mysql -D icinga2 -N -e "${mysql_ServiceDJ_ServicesTotal}"`

###mail格式整理###
  sendMessage=`echo "
  --[ServiceDJ 告警通知]---------------------
  告警時間:${TODAY}
  異常裝置:${get_HOSTNAME}(${IpHandle})
  異常服務:${deviceType}
  --故障說明與描述:--------------------------
  完整資訊:
  ${mailMessage}
  -------------------------------------------
  
  --[ServiceDJ 聯絡資訊]---------------------
  客戶中文名稱: ${customerInfo_CompanyName}
  客戶地址: ${customerInfo_CompanyAddress}
  客戶電話: ${customerInfo_CompanyPhoneNumber}
  客戶聯絡人: ${customerInfo_CompanyContactor}

  --[ServiceDJ 系統資訊]---------------------
  ServiceDJ版本: ${ServiceDJ_version}
  裝置異常數: ${ServiceDJ_HostErrorStatus}/${ServiceDJ_HostsTotal}
  服務異常數: ${ServiceDJ_ServiceErrorStatus}/${ServiceDJ_ServicesTotal}
  -------------------------------------------"`
#  echo $sendMessage > $testfile
  echo $get_HOSTNAME >$testfile
  echo $IpHandle >>$testfile  
  echo $get_ipFrom >>$testfile
  echo $emaillist >>$testfile
###寄mail
#  for i in $emaillist
#  do
#  done
  su icinga <<EOF
  echo "$sendMessage" | mutt -s "[ServiceDJ 通知]TrapMessage_HostName:$get_HOSTNAME _HostIP:$IpHandle _Title:$get_ipFrom" -- $emaillist;
  exit;
EOF
 fi
done



#echo "*****************************************************************************************" >> $logfile
#echo "${traptest1}" >> $logfile
#echo "${get_HOSTNAME}" >> $logfile
#echo "${ServiceName}" >> $logfile
#echo "${db_insert_time}" >> $logfile
#echo "${host}" >> $logfile
#echo "${Statu}" >> $logfile
#echo "${get_ipFrom}" >> $logfile
#echo "${get_value}" >> $logfile
#echo "${IpHandle}" >> $logfile
#echo "${deviceType}" >> $logfile
#echo "${uniformNumber}" >> $logfile
#echo "echo $mailMessage | mutt -s HostName:$get_HOSTNAME HostIP:$IpHandle TrapMessage -- $email" >> $logfile
###


