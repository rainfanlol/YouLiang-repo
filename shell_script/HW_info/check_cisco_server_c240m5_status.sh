#!/bin/bash
#ver.1
#將cisco零件狀態存入資料庫

SNMP_version=$1
SNMP_community=$2
HostIP=$3
port=$4
choice=$5
log_level=$6
Warning=$7
Critical=$8
CM="snmpwalk -Oqv -v $SNMP_version -c $SNMP_community -m all $HostIP:$port"
MCM="snmpwalk -v $SNMP_version -c $SNMP_community -m all $HostIP:$port"
ti=".1.3.6.1.4.1.9.9.719."

### APIname ###

API="check_cisco_server_c240m5_status"

### oid value ###
#sysOID=${ti}5.1.1.1
#sysOSOID=${ti}5.2.1.0
cpuOID=${ti}1.41.9.1.9
memOID=${ti}1.30.11.1.13
#tempOID=${ti}5.4.700.20.1.5
powerOID=${ti}1.15.56.1.7
#nicOID=${ti}5.4.1100.90.1.3
diskOID=${ti}1.45.4.1.18
#batOID=${ti}5.4.600.50.1.5
coolOID=${ti}1.15.12.1.9
#raidOID=${ti}5.5.1.20.130.1.1.38
#virtualdiskOID=${ti}5.5.1.20.140.1.1.20
pciOID=${ti}1.45.1.1.6
#enclosureOID=${ti}5.5.1.20.130.3.1.24

### oid key ###
#sysnameOID=${ti}5.1.1.1
sysosnameOID=${ti}1.9.6.1.6
#memnameOID=${ti}1.30.11.1.1.3
#tempnameOID=${ti}5.4.700.20.1.8
coolnameOID=${ti}1.15.12.1.7
#batnameOID=${ti}5.4.600.50.1.7
#raidnameOID=${ti}5.5.1.20.130.1.1.2
#cpunameOID=${ti}5.4.1100.32.1.7
#nicnameOID=${ti}5.4.1100.90.1.6
#powernameOID=${ti}5.4.600.12.1.8
disknameOID=${ti}1.45.4.1.3
#virtualdisknameOID=${ti}5.5.1.20.140.1.1.36
pcinameOID=${ti}1.45.1.1.5
#enclosurenameOID=${ti}5.5.1.20.130.3.1.2

### for mem name oid ###




if [ "${port}" == " " ]; then
        port=161
fi

dateTime=`date +%Y/%m/%d\ %H:%M:%S`
unset total_status

sqlcounter=0;

### 匯入函數庫  ###
. /etc/icinga2/scripts/function_insert.sh
. /etc/icinga2/scripts/function_MySQL.sh

########## call object id function ##########
#. /etc/icinga2/scripts/function_insert.sh

dpname=$(_getHost_display_name $3)
objectid=$(_getHost_object_id_fromDisName $3 $dpname)
#echo $objectid
#dpname=123
#objectid=456



########## status function ##########
function_status(){
        if [ "$1" == "ok" ] || [ "$1" == "1" ];
                then
                        echo 0;
                elif [ "$1" == "unknown" ] || [ "$1" == "0" ];
			then
                        	echo 1;
                	else
                        	echo 2;
                        	total_status=3;
        fi
}

###total status function###
#total_status_function(){



#}
### 刪舊資料  ###
#timeout = 60
delQuery="DELETE FROM mirle_mon_Server_CISCO WHERE icin_host_object_id = '${objectid}' and Device = '${dpname}' and APIname='${API}'"
_runTransactSQL "${delQuery}"



########## mysql function ##########
function_mysql(){
        count=0;
        for c in $(seq 1 1 $(echo -e "$1" | wc -l));
                do
                        count=$(($count+1));
                        i=$(echo -e "$1" | sed -n ${c}p)
                        sqlkey[$count]=$(echo -e "$i" | awk -F "@" '{print $1}');
                        sqlvalue[$count]=$(echo -e "$i" | awk -F "@" '{print $2}');
                done

        unset sqlQuerykey;
        unset sqlQueryvalue;
        for i in $(seq 1 1 $count);
                do
                        if [ "$i" != "$count" ];
                                then
                                        sqlQuerykey=$(echo -e "$sqlQuerykey ${sqlkey[$i]},");
                                        sqlQueryvalue=$(echo -e "$sqlQueryvalue '${sqlvalue[$i]}',");
                                else
                                        sqlQuerykey=$(echo -e "$sqlQuerykey ${sqlkey[$i]}");
                                        sqlQueryvalue=$(echo -e "$sqlQueryvalue '${sqlvalue[$i]}'");
                        fi
                done

        unset sqlQuery;
        sqlQuery="INSERT INTO mirle_mon_Server_CISCO($sqlQuerykey) VALUES ($sqlQueryvalue);"
        sudo mysql -D icinga2 -e "$sqlQuery"

#        sqlcounter=$(($sqlcounter+1));

}


#echo -e "檢測dell電腦IP:$HostIP"

###OS NAME###
#sysname=$($CM $sysnameOID)
osname=$($CM $sysosnameOID)
#sysstatus=$($CM $sysOSOID)
#sysnamekey=$(echo -e $osname)
#sysnamevalue=$(echo -e "$sysstatus")
sqlcounter=0
#echo -e "rac_name:"$sysname
#echo -e "伺服器OS名稱:"$osname
#echo -e "伺服器狀態:"$sysstatus
#伺服器系統狀態:$sysstatus
#echo -e "$sysnamevalue"
sysNamesql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@SystemName\ndatavalue@${osname}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#echo $sysNamesql
#echo -e $sysNamesql


function_mysql "$sysNamesql"


###CPU###
#cpuname=$($CM $cpunameOID)
cpuStatus=$($CM $cpuOID | sed 's/operable/ok/g')
cpuNum=$(echo -e "$cpuStatus" | wc -l)
cputotalstatus=0

for i in $(seq 1 1 $cpuNum);
        do
                sqlcounter='1,'$i
                cpuStatuskey[$i]=$(echo -e "CPU$i")
#                cpunamevalue[$i]=$(echo -e "$cpuname" | sed -n ${i}p)
                cpuStatusvalue[$i]=$(echo -e "$cpuStatus" | sed -n ${i}p)
                cpucode[$i]=$(function_status ${cpuStatusvalue[$i]})
                cpusql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${cpuStatuskey[$i]}\ndatavalue@\"${cpuStatusvalue[$i]}\"\nstatus@${cpucode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")

#                echo $cpusql
                function_mysql "$cpusql"                
#               echo -e ${cpunamevalue[$i]}"狀態:"${cpuStatusvalue[$i]}
                if [[ ${cpucode[$i]} > $cputotalstatus ]] ; then
                cputotalstatus=${cpucode[$i]}
                fi
        done

sqlcounter=1
titlecpusql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@CPU\ndatavalue@ok\nstatus@${cputotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$titlecpusql"
#               echo $titlecpusql


###記憶體###
#memname=$($CM $memnameOID | sed -e '/NA/d')
memoryhandle=$($MCM $memOID | sed 's/operable(1)/ok/g'  | sed 's/CISCO-UNIFIED-COMPUTING-MEMORY-MIB::cucsMemoryUnitOperState/DIMM/g' | sed 's/INTEGER:/@/g' | sed 's/\.1 =/.A1/g' | sed 's/\.2 =/.A2/g' | sed 's/\.3 =/.B1/g' | sed 's/\.4 =/.B2/g' | sed 's/\.5 =/.C1/g' | sed 's/\.6 =/.C2/g' | sed 's/\.7 =/.D1/g' | sed 's/\.8 =/.D2/g' | sed 's/\.9 =/.E1/g' | sed 's/\.10 =/.E2/g' | sed 's/\.11 =/.F1/g' | sed 's/\.12 =/.F2/g' | sed 's/\.13 =/.G1/g' | sed 's/\.14 =/.G2/g' | sed 's/\.15 =/.H1/g' | sed 's/\.16 =/.H2/g' | sed 's/\.17 =/.J1/g' | sed 's/\.18 =/.J2/g' | sed 's/\.19 =/.K1/g' | sed 's/\.20 =/.K2/g' | sed 's/\.21 =/.L1/g' | sed 's/\.22 =/.L2/g' | sed 's/\.23 =/.M1/g' | sed 's/\.24 =/.M2/g' | sed -e '/unknown/d')
#memoryStatus=$($CM $memOID | sed -e '/unknown/d' | sed 's/operable/ok/g')
memname=$(echo -e "$memoryhandle"| awk -F " @ " '{print $1}');
memoryStatus=$(echo -e "$memoryhandle" | awk -F " @ " '{print $2}');


memoryNum=$(echo -e "$memoryhandle" | wc -l)
memtotalstatus=0

for i in $(seq 1 1 $memoryNum);
        do
                sqlcounter='2,'$i 
#               memoryStatuskey[$i]=$(echo -e "memory$i")
                memorynamevalue[$i]=$(echo -e "$memname" | sed -n ${i}p)
                memoryStatusvalue[$i]=$(echo -e "$memoryStatus" | sed -n ${i}p)
                memcode[$i]=$(function_status ${memoryStatusvalue[$i]})
                memsql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${memorynamevalue[$i]}\ndatavalue@\"${memoryStatusvalue[$i]}\"\nstatus@${memcode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$memsql"
#                echo $memsql
                if [[ ${memcode[$i]} > $memtotalstatus ]] ; then
                memtotalstatus=${memcode[$i]}
                fi
        done

sqlcounter=2
titlememsql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@Memory\ndatavalue@ok\nstatus@${memtotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$titlememsql"
#               echo $titlememsql

###溫度感測器##

#tempname=$($CM $tempnameOID)
#tempStatus=$($CM $tempOID)
#tempNum=$(echo -e "$tempStatus" | wc -l)
#for i in $(seq 1 1 $tempNum);
#        do
#                tempStatuskey[$i]=$(echo -e "Temp$i")
#                tempnamevalue[$i]=$(echo -e "$tempname" | sed -n ${i}p)
#                tempStatusvalue[$i]=$(echo -e "$tempStatus" | sed -n ${i}p)
#                echo -e ${tempnamevalue[$i]}"溫度狀態:"${tempStatusvalue[$i]}
#        done

###冷卻裝置風扇###
coolname=$($CM $coolnameOID | sed 's/_SPEED//g')
coolStatus=$($CM $coolOID | sed 's/operable/ok/g' | sed -e '/removed/d')
coolNum=$(echo -e "$coolStatus" | wc -l)
cooltotalstatus=0
for i in $(seq 1 1 $coolNum);
        do
                sqlcounter='3,'$i
#                coolStatuskey[$i]=$(echo -e "cool$i")
                coolnamevalue[$i]=$(echo -e "$coolname" | sed -n ${i}p)
                coolStatusvalue[$i]=$(echo -e "$coolStatus" | sed -n ${i}p)
                coolcode[$i]=$(function_status ${coolStatusvalue[$i]})
                coolsql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${coolnamevalue[$i]}\ndatavalue@\"${coolStatusvalue[$i]}\"\nstatus@${coolcode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$coolsql"
#                echo $coolsql
                if [[ ${coolcode[$i]} > $cooltotalstatus ]] ; then
                cooltotalstatus=${coolcode[$i]}
                fi
        done

sqlcounter=3
titlecoolsql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@Fan\ndatavalue@ok\nstatus@${cooltotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$titlecoolsql"
#                echo $titlecoolsql


###電源供應器###
#powername=$($CM $powernameOID)
powerStatus=$($CM $powerOID | sed 's/operable/ok/g')
powerNum=$(echo -e "$powerStatus" | wc -l)
powertotalstatus=0
for i in $(seq 1 1 $powerNum);
        do
                sqlcounter='4,'$i
                powerStatuskey[$i]=$(echo -e "PSU$i")
#                powernamevalue[$i]=$(echo -e "$powername" | sed -n ${i}p)
                powerStatusvalue[$i]=$(echo -e "$powerStatus" | sed -n ${i}p)
#               echo -e "電源供應器"${powernamevalue[$i]}"狀態:"${powerStatusvalue[$i]}
                powercode[$i]=$(function_status ${powerStatusvalue[$i]})
                powersql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${powerStatuskey[$i]}\ndatavalue@\"${powerStatusvalue[$i]}\"\nstatus@${powercode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$powersql"
#                 echo $powersql
                if [[ ${powercode[$i]} > $powertotalstatus ]] ; then
                powertotalstatus=${powercode[$i]}
                fi
        done

sqlcounter=4
titlepowersql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@PSU\ndatavalue@ok\nstatus@${powertotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$titlepowersql"
#                 echo $titlepowersql

###raid卡###
#raidname=$($CM $raidnameOID)
#raidNum=$(echo -e "$raidStatus" | wc -l)
#for i in $(seq 1 1 $raidNum);
#        do
#                enicStatuskey[$i]=$(echo -e "Embedded NIC$i")
#                enicStatusvalue[$i]=$(echo -e "$enicStatus" | sed -n ${i}p)
#                eniccode[$i]=$(function_status ${enicStatusvalue[$i]})
#                enicsql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${enicStatuskey[$i]}\ndatavalue@\"${enicStatusvalue[$i]}\"\nstatus@${eniccode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#                function_mysql "$enicsql"
#                echo -e "controller"${raidname}"狀態:"${raidStatus}
#        done

###網路卡###
#nicname=$($CM $nicnameOID | sed 's/"//g')
#nicStatus=$($CM $nicOID)
#nicNum=$(echo -e "$nicStatus" | wc -l)
#nictotalstatus=0
#for i in $(seq 1 1 $nicNum);
#        do
#                sqlcounter='5,'$i
#                nicStatuskey[$i]=$(echo -e "NIC$i")
#                nicnamevalue[$i]=$(echo -e "$nicname" | sed -n ${i}p)
#                nicStatusvalue[$i]=$(echo -e "$nicStatus" | sed -n ${i}p)
#               echo -e "網路卡"${nicnamevalue[$i]}"狀態:"${nicStatusvalue[$i]}
#                niccode[$i]=$(function_status ${nicStatusvalue[$i]})
#                nicsql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${nicnamevalue[$i]}\ndatavalue@\"${nicStatusvalue[$i]}\"\nstatus@${niccode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#                function_mysql "$nicsql"
#                if [[ ${niccode[$i]} > $nictotalstatus ]] ; then
#                $nictotalstatus=${niccode[$i]}
#                fi
#        done

#sqlcounter=5
#titlenicsql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@NIC\ndatavalue@ok\nstatus@${nictotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#                function_mysql "$titlenicsql"

###磁碟###
#diskname=$($CM $disknameOID)
diskStatus=$($CM $diskOID | sed -e '/unknown/d' | sed 's/online/ok/g')
diskNum=$(echo -e "$diskStatus" | wc -l)
disktotalstatus=0
for i in $(seq 1 1 $diskNum);
        do
                sqlcounter='5,'$i
                diskStatuskey[$i]=$(echo -e "Pd-$i")
#                disknamevalue[$i]=$(echo -e "$diskname" | sed -n ${i}p)
                diskStatusvalue[$i]=$(echo -e "$diskStatus" | sed -n ${i}p)
#               echo -e "磁碟"${disknamevalue[$i]}"狀態:"${diskStatusvalue[$i]}
                diskcode[$i]=$(function_status ${diskStatusvalue[$i]})
                disksql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${diskStatuskey[$i]}\ndatavalue@\"${diskStatusvalue[$i]}\"\nstatus@${diskcode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$disksql"
#                echo $disksql
                if [[ ${diskcode[$i]} > $disktotalstatus ]] ; then
                disktotalstatus=${diskcode[$i]}
                fi
        done

sqlcounter=5
titledisksql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@Disk\ndatavalue@ok\nstatus@${disktotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$titledisksql"
#                echo $titledisksql
###虛擬磁碟###
#virtualdiskname=$($CM $virtualdisknameOID)
#virtualdiskStatus=$($CM $virtualdiskOID)
#virtualdiskNum=$(echo -e "$virtualdiskStatus" | wc -l)
#virtualdisktotalstatus=0
#for i in $(seq 1 1 $virtualdiskNum);
#        do
#                sqlcounter='7,'$i
#                virtualdiskStatuskey[$i]=$(echo -e "virtualDisk$i")
#                virtualdisknamevalue[$i]=$(echo -e "$virtualdiskname" | sed -n ${i}p)
#                virtualdiskStatusvalue[$i]=$(echo -e "$virtualdiskStatus" | sed -n ${i}p)
#                virtualdiskcode[$i]=$(function_status ${virtualdiskStatusvalue[$i]})
#                virtualdisksql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${virtualdisknamevalue[$i]}\ndatavalue@\"${virtualdiskStatusvalue[$i]}\"\nstatus@${virtualdiskcode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#                echo -e "虛擬磁碟"${virtualdisknamevalue[$i]}"狀態:"${virtualdiskStatusvalue[$i]}
#                function_mysql "$virtualdisksql"
#                if [[ ${virtualdiskcode[$i]} > $virtualdisktotalstatus ]] ; then
#                $virtualdisktotalstatus=${virtualdiskcode[$i]}
#                fi
#        done

#sqlcounter=7
#titlevirtualdisksql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@Virtualdisk\ndatavalue@ok\nstatus@${virtualdisktotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#                function_mysql "$titlevirtualdisksql"

###電池###
#CBname=$($CM $batnameOID | sed 's/"//g')
#CBStatus=$($CM $batOID)
#CBNum=$(echo -e "$CBStatus" | wc -l)
#CBtotalstatus=0
#for i in $(seq 1 1 $CBNum);
#        do
#                sqlcounter='6,'$i
#               CBStatuskey[$i]=$(echo -e "CacheBattery$i")
#                CBnamevalue[$i]=$(echo -e "$CBname" | sed -n ${i}p)
#                CBStatusvalue[$i]=$(echo -e "$CBStatus" | sed -n ${i}p)
#               echo -e "電池"${CBnamevalue[$i]}"狀態:"${CBStatusvalue[$i]}
#                CBcode[$i]=$(function_status ${CBStatusvalue[$i]})
#               CBsql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${CBnamevalue[$i]}\ndatavalue@\"${CBStatusvalue[$i]}\"\nstatus@${CBcode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#                function_mysql "$CBsql"
#                if [[ ${CBcode[$i]} > $CBtotalstatus ]] ; then
#                $CBtotalstatus=${CBcode[$i]}
#                fi
#        done

#sqlcounter=6
#titleCBsql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@CacheBattery\ndatavalue@ok\nstatus@${CBtotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#                function_mysql "$titleCBsql"

###pci_device###
pciname=$($CM $pcinameOID)
pciStatus=$($CM $pciOID | sed 's/operable/ok/g')
pciNum=$(echo -e "$pciStatus" | wc -l)
pcitotalstatus=0
for i in $(seq 1 1 $pciNum);
        do
                sqlcounter='6,'$i
#               pciStatuskey[$i]=$(echo -e "pci$i")
                pcinamevalue[$i]=$(echo -e "$pciname" | sed -n ${i}p)
                pciStatusvalue[$i]=$(echo -e "$pciStatus" | sed -n ${i}p)
                pcicode[$i]=$(function_status ${pciStatusvalue[$i]})
#               echo -e "pci:"${pcinamevalue[$i]}"狀態:"${pciStatusvalue[$i]}
                pcisql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${pcinamevalue[$i]}\ndatavalue@\"${pciStatusvalue[$i]}\"\nstatus@${pcicode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$pcisql"
#                echo $pcisql
                if [[ ${pcicode[$i]} > $pcitotalstatus ]] ; then
                pcitotalstatus=${pcicode[$i]}
                fi
        done

sqlcounter=6
titlepcisql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@PCI\ndatavalue@ok\nstatus@${pcitotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
                function_mysql "$titlepcisql"




### 統一時間  ###
updateQuery="UPDATE mirle_mon_Server_CISCO SET insert_date = \"${dateTime}\";"
_runTransactSQL "${updateQuery}"

#               echo $titlepcisql
###enclosure###
#enclosurename=$($CM $enclosurenameOID)
#enclosureStatus=$($CM $enclosureOID)
#enclosureNum=$(echo -e "$enclosureStatus" | wc -l)
#entotalstatus=0
#for i in $(seq 1 1 $enclosureNum);
#        do
#                sqlcounter='10,'$i
#                enclosureStatuskey[$i]=$(echo -e "enclosure$i")
#                enclosurenamevalue[$i]=$(echo -e "$enclosurename" | sed -n ${i}p)
#                enclosureStatusvalue[$i]=$(echo -e "$enclosureStatus" | sed -n ${i}p)
#                enclosurecode[$i]=$(function_status ${enclosureStatusvalue[$i]})
#               echo -e "enclosure:"${enclosurenamevalue[$i]}"狀態:"${enclosureStatusvalue[$i]}
#                enclosuresql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@${enclosurenamevalue[$i]}\ndatavalue@\"${enclosureStatusvalue[$i]}\"\nstatus@${enclosurecode[$i]}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#                function_mysql "$enclosuresql"
#                if [[ ${enclosurecode[$i]} > $entotalstatus ]] ; then
#                $entotalstatus=${enclosurecode[$i]}
#                fi
#        done

#sqlcounter=10
#titleensql=$(echo -e "icin_host_object_id@${objectid}\nDevice@${dpname}\nAPIname@${API}\ndatakey@Enclosure\ndatavalue@ok\nstatus@${entotalstatus}\nlayer@${sqlcounter}\ninsert_date@${dateTime}")
#                function_mysql "$titleensql"

########## echo all value ##########
#echo -e "$sysnamekey:$sysnamevalue"
<<ooo
for i in $(seq 1 1 $cpuNum);
        do
                echo -e "${cpuStatuskey[$i]}:${cpuStatusvalue[$i]}";
        done
for i in $(seq 1 1 $memoryNum);
        do
                echo -e "${memorynamevalue[$i]}:${memoryStatusvalue[$i]}";
        done
for i in $(seq 1 1 $powerNum);
        do
                echo -e "${powerStatuskey[$i]}:${powerStatusvalue[$i]}";
        done
for i in $(seq 1 1 $coolNum);
        do
                echo -e "${coolnamevalue[$i]}:${coolStatusvalue[$i]}";
        done
for i in $(seq 1 1 $pciNum);
        do
                echo -e "${pcinamevalue[$i]}:${pciStatusvalue[$i]}";
        done
for i in $(seq 1 1 $nicNum);
        do
                echo -e "${nicnamevalue[$i]}:${nicStatusvalue[$i]}";
        done
for i in $(seq 1 1 $diskNum);
        do
                echo -e "${diskStatuskey[$i]}:${diskStatusvalue[$i]}";
        done
for i in $(seq 1 1 $CBNum);
        do
                echo -e "${CBnamevalue[$i]}:${CBStatusvalue[$i]}";
        done
for i in $(seq 1 1 $virtualdiskNum);
        do
                echo -e "${virtualdisknamevalue[$i]}:${virtualdiskStatusvalue[$i]}";
        done
for i in $(seq 1 1 $enclosureNum);
        do
                echo -e "${enclosurenamevalue[$i]}:${enclosureStatusvalue[$i]}";
        done

ooo
########## return error code ##########
case total_status in
        0)
                echo "000"
                exit 0
                ;;
        1)
                echo "001"
                exit 1
                ;;
        2)
                echo "002"
                exit 2
                ;;
esac

