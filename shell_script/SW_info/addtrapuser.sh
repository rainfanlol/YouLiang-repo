#!/bin/bash
#EngineID=$f1
#username=$f2
#mode=$f3


filename="/etc/icinga2/scripts/trap/phptrap.txt"
while [ 1 ]; do


#filename="/etc/icinga2/scripts/trap/phptrap.txt"
 
 if [ -s "$filename" ]
 then
  list=`cat /etc/icinga2/scripts/trap/phptrap.txt`
  service snmptrapd stop
  for val in $list
  do
   while IFS=":" read -r f1 f2 f3;
    do
     case $f3 in
      1) 
         #$f2==`echo${f2,,}`
         EngineIDlist+=$f2" "
         sed -i '21i authUser log,execute '"$f2"' noauth' /etc/snmp/snmptrapd.conf
         sed -i '21i createUser -e '"$f1"' '"$f2"'' /etc/snmp/snmptrapd.conf
         sed -i '1d' /etc/icinga2/scripts/trap/phptrap.txt
         #sed -i '/'"$f2"'/d' /etc/snmp/snmptrapd.conf
      ;;
      2) 
         EID=`echo ${f1,,}`
         EngineIDlist+=$f2" "
         sed -i '/'"$EID"'/d' /var/lib/net-snmp/snmptrapd.conf
        #sed -i '/0x'"$EngineID"'/d' /etc/snmp/snmptrapd.conf
         sed -i '21i authUser log,execute '"$f2"' noauth' /etc/snmp/snmptrapd.conf
         sed -i '21i createUser -e '"$f1"' '"$f2"'' /etc/snmp/snmptrapd.conf
         sed -i '1d' /etc/icinga2/scripts/trap/phptrap.txt
         #sed -i '/'"$f2"'/d' /etc/snmp/snmptrapd.conf
      ;;
      3) 
         EID=`echo ${f1,,}`
         sed -i '/'"$EID"'/d' /var/lib/net-snmp/snmptrapd.conf
         #sed -i '/'"$f2"'/d' /etc/snmp/snmptrapd.conf
         sed -i '1d' /etc/icinga2/scripts/trap/phptrap.txt
      ;;
      *)  echo 'You do not select a number between 1 to 3'
      ;;
     esac

   done < /etc/icinga2/scripts/trap/phptrap.txt
  done
  service snmptrapd start
  service snmptrapd restart
  for vals in $EngineIDlist
   do
    sed -i '/'"$vals"'/d' /etc/snmp/snmptrapd.conf
   done
  unset EngineIDlist

 else
   sleep 1
 fi

done
