#!/bin/ash
tmpData=`grep 'lcd_set_enginetime\|Unknown User\|secName\|secLevel\|udpbase:recv: got source addr:' /var/log/snmptrapd.log`
trapEngineID=`echo "${tmpData}" |grep boots|awk -F ':\ ' '{print $2}'|sed s/engineID//g|sed s/\ //g`
trapUser=`echo "${tmpData}" |grep usm|awk -F '(' '{print $2}'|awk -F ')' '{print $1}'`
trapLevel=`echo "${tmpData}" |grep secName|awk -F 'secLevel:' '{print $2}'|awk -F ')' '{print $1}'`
trapHostAddr=`echo "${tmpData}" |grep 'udpbase:recv: got source addr:'|awk '{print $5}'`

_debug()
{
echo "
# trapEngineID #
################
$trapEngineID
"
echo "
# trapUser #
############
$trapUser
"
echo "
# trapLevel #
#############
$trapLevel
"
echo "
# trapHostAddr #
################
$trapHostAddr
"
exit 0
}
#_debug

snmptrapActiveHostsAddress=`mysql -N -e "select address from mirle_view_AllActiveHostsAddress WHERE ServiceType='Snmptrap'"`

_restart()
{
  # remove /var/lib/net-snmp/snmptrapd.conf after kill snmptrapd process 2 seconds (first time to kill snmptrapd process)
  # create /var/lib/net-snmp/snmptrapd.conf after kill snmptrapd process second times
  # it have to run 2 times snmptrapd process to reset snmptrapd.conf
  snmptrapd_start_pid=`ps -ef|grep trap-mibs|awk '{print $1}'|head -n 1`;
  kill $snmptrapd_start_pid;
  sleep 2;
  rm -f /var/lib/net-snmp/snmptrapd.conf;
  ls -l /var/lib/net-snmp/snmptrapd.conf;
  /usr/sbin/snmptrapd -M +/usr/share/snmp/trap-mibs -m ALL -c /etc/snmp/snmptrapd.conf -D -Loe -Lf /var/log/snmptrapd.log;
  snmptrapd_start_pid=`ps -ef|grep trap-mibs|awk '{print $1}'|head -n 1`;
  kill $snmptrapd_start_pid;
  /usr/sbin/snmptrapd -M +/usr/share/snmp/trap-mibs -m ALL -c /etc/snmp/snmptrapd.conf -D -Loe -Lf /var/log/snmptrapd.log;
}

_checkActiveHostsAddress()
{
  checkIP=$1
  if [ ! -z ${checkIP} ];then
    checkActiveHostsAddressResult=0
    for j in `echo "${snmptrapActiveHostsAddress}"`;do
      if [ ${j} == ${checkIP} ];then
        checkActiveHostsAddressResult=1
      fi
    done
  fi
}

count=1
restartKey=0
echo "execute date: `date`" >> /var/log/updateTrapUser.log
checktrapEngineIDsize=`echo "${trapEngineID}"|wc -l`
for i in `echo "${trapEngineID}"`;do
  trapUser_tmp=`echo "${trapUser}"|sed -n ${count}p`
  trapLevel_tmp=`echo "${trapLevel}"|sed -n ${count}p`
  trapHostAddr_tmp=`echo "${trapHostAddr}"|sed -n ${count}p`
  _checkActiveHostsAddress ${trapHostAddr_tmp}

_debug2()
{
echo "
trapEngineID: ${i}
trapUser_tmp: ${trapUser_tmp}
trapLevel_tmp: ${trapLevel_tmp}
trapHostAddr_tmp: ${trapHostAddr_tmp}"
count=$((count+1))
continue
}
#_debug2

  # if user/level/address are empty, then continue
  # if address is not allowed in the ActiveHostsAddress list, then continue
  # there is no user in snmptrapd.conf, and user/level/address are empty, then restart snmptrapd service
  if [ -z ${i} ] || [ -z ${trapUser_tmp} ] || [ -z ${trapLevel_tmp} ] || [ -z ${trapHostAddr_tmp} ] || [ ${checkActiveHostsAddressResult} -ne 1 ];then
    checkUser=`cat /etc/snmp/snmptrapd.conf|grep 'createUser\|authUser'|wc -l`
    if [ ${checkUser} -eq 0 ] || [ ${checktrapEngineIDsize} -ge 100 ];then
      _restart
      echo "restart snmptrapd"
      echo "restart snmptrapd(break)" >> /var/log/updateTrapUser.log
      break
    else
      echo "skip this step"
      echo "skip this step(continue)" >> /var/log/updateTrapUser.log
      continue
    fi
  else
    # if user and engineid are exist, then skip this step
    checkUser=`cat /etc/snmp/snmptrapd.conf|grep ${trapUser_tmp}|wc -l`
    checkEngineID=`cat /etc/snmp/snmptrapd.conf|grep ${i}|wc -l`
    if [ ${checkUser} -eq 0 ] || [ ${checkEngineID} -eq 0 ];then
      if [ ${trapLevel_tmp} == authPriv ];then
        echo "createUser -e 0x${i} ${trapUser_tmp} SHA p@ssw0rd AES p@ssw0rd # trapHostAddr_tmp: ${trapHostAddr_tmp}" >> /etc/snmp/snmptrapd.conf
        echo "authUser log,execute,net ${trapUser_tmp} # trapHostAddr_tmp: ${trapHostAddr_tmp}" >> /etc/snmp/snmptrapd.conf
      else
      _debug3()
      {
        echo "createUser -e 0x${i} ${trapUser_tmp} # trapHostAddr_tmp: ${trapHostAddr_tmp}"
        echo "authUser log,execute,net ${trapUser_tmp} ${trapLevel_tmp} # trapHostAddr_tmp: ${trapHostAddr_tmp}"
        count=$((count+1))
        continue
      }
      #_debug3

        echo "createUser -e 0x${i} ${trapUser_tmp} # trapHostAddr_tmp: ${trapHostAddr_tmp}" >> /etc/snmp/snmptrapd.conf
        echo "authUser log,execute,net ${trapUser_tmp} ${trapLevel_tmp} # trapHostAddr_tmp: ${trapHostAddr_tmp}" >> /etc/snmp/snmptrapd.conf
      fi

      # restart snmptrapd service
      restartKey=1
      echo "createUser ${trapUser_tmp}, engineID 0x${i}, trapHostAddr_tmp ${trapHostAddr_tmp}" >> /var/log/updateTrapUser.log
    fi
  fi
  echo "${i}, ${trapUser_tmp}, ${trapLevel_tmp}", ${trapHostAddr_tmp} >> /var/log/updateTrapUser.log
  echo "===============================================" >> /var/log/updateTrapUser.log
  tail -n 4 /var/log/updateTrapUser.log
  count=$((count+1))
done

# filter unactive host address, and reset active host address
filterIP=`echo ${snmptrapActiveHostsAddress}|sed s/\ /'\\\|'/g`
origSetting=`cat /etc/snmp/snmptrapd.conf|grep -v trapHostAddr_tmp`
filterSetting=`cat /etc/snmp/snmptrapd.conf|grep "${filterIP}"`
rm -f /etc/snmp/snmptrapd.conf.tmp
echo "${origSetting}" > /etc/snmp/snmptrapd.conf.tmp
if [ ! -z ${filterIP} ];then
  echo "${filterSetting}" >> /etc/snmp/snmptrapd.conf.tmp
fi
replaceKeyResult=`diff /etc/snmp/snmptrapd.conf /etc/snmp/snmptrapd.conf.tmp |wc -l`
if [ ${replaceKeyResult} -gt 0 ];then
  mv /etc/snmp/snmptrapd.conf.tmp /etc/snmp/snmptrapd.conf
  echo "reset snmptrapd.conf" >> /var/log/updateTrapUser.log
  echo "===============================================" >> /var/log/updateTrapUser.log
  restartKey=1
fi

# check log file size, if size over 10MB then tack 500 rows and put back to the file
if [ -e /var/log/updateTrapUser.log ];then
  logFileSize=`du /var/log/updateTrapUser.log |awk '{print $1}'`
  if [ ${logFileSize} -ge 10240 ];then
    keep500rows=`tail -n 500 /var/log/updateTrapUser.log`
    echo "${keep500rows}" > /var/log/updateTrapUser.log
  fi
else
  # if log file is not exist (snmptrapd container is first execute)
  logFileSize=0
  echo "/var/log/updateTrapUser.log is not exist. Now is created this file." > /var/log/updateTrapUser.log
fi

# check snmptrapd log file size, if size over 10MB then tack 500 rows and put back to the file
if [ -e /var/log/snmptrapd.log ];then
  logFileSize=`du /var/log/snmptrapd.log |awk '{print $1}'`
  if [ ${logFileSize} -ge 10240 ];then
    restartKey=1
  fi
fi

# restart snmptrapd service by restartKey
if [ ${restartKey} -eq 1 ];then
  _restart
  restartKey=0
fi

