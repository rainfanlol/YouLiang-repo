#!/bin/bash

#parameter
TokenPath="https://oct1/api/Account/Authenticate"
UserName="\"admin\""
password="\"p@ssw0rd\""
LastDay=`date -d last-day +%Y-%m-%d`
NowTime=`date -d '480 minute ago' +%Y-%m-%dT%H`
NowTimeMin=`date -d '480 minute ago' +%M`
NowTimeSec=`date -d '480 minute ago' +%S`
FiveMinAgo=`date -d '485 minute ago' +%Y-%m-%dT%H`
FiveMinAgoMin=`date -d '485 minute ago' +%M`
FiveMinAgoSec=`date -d '485 minute ago' +%S`
timestamp=`date +%Y-%m-%dT%H:%M:%S.000Z`
ESpath="http://172.16.97.65:9200"
indexName="jobstatistics"
tempPath="/root/you/jobstatistics/"


GetToken=`curl -k -X POST ${TokenPath} -H "accept: application/json" -H "Content-Type: application/json" -d '{ "tenancyName": "Default", "usernameOrEmailAddress":'"${UserName}"', "password":'"${password}"'}'| awk -F '"result":"' '{print $2}'|awk -F '","' '{print $1}'`

GetRawdata=`curl -k -X GET "https://oct1/odata/Jobs?%24filter=EndTime%20gt%20${FiveMinAgo}%3A${FiveMinAgoMin}%3A${FiveMinAgoSec}.000Z&%24select=EndTime%2CState%2CReleaseName%2CHostMachineName" -H "accept: application/json" -H "Authorization: Bearer ${GetToken}"`
#https://oct1/odata/Jobs?%24filter=EndTime%20gt%202021-10-08T02%3A44%3A00.000Z&%24select=EndTime%2CState%2CReleaseName%2CHostMachineName

#echo ${GetRawdata}

echo "${GetRawdata}"|python -m json.tool > ${tempPath}Jobs_Get_rawData
cat ${tempPath}Jobs_Get_rawData |grep '"CreationTime": "\|"HostMachineName": "\|"ReleaseName": "\|"StartTime": "\|"EndTime": "\|"State": "\|\ },'|sed 's/\ },/---------/g'|tr -d ' ' > ${tempPath}Jobs_Get_filterData
echo "---------" >> ${tempPath}Jobs_Get_filterData
#cat ${tempPath}Jobs_Get_filterData > test.log
filterData_row=`cat ${tempPath}Jobs_Get_filterData|wc -l`
reconstructionJson=""
PUT_BODY=""
count=1

while [ ${count} -le ${filterData_row} ]
do

  filterData_head=`cat ${tempPath}Jobs_Get_filterData|grep -n EndTime|head -n 1|awk -F ':' '{print $1}'`
  filterData_foot=`cat ${tempPath}Jobs_Get_filterData|grep -n "\-\-\-\-\-\-\-\-\-"|head -n 1|awk -F ':' '{print $1}'`
  if [ -z ${filterData_head} ] || [ -z ${filterData_foot} ];then
    exit 0
  else
    reconstructionJson=`cat ${tempPath}Jobs_Get_filterData|sed -n ${filterData_head},${filterData_foot}p`
  fi

  #timestamp=`date +%Y-%m-%dT%H:%M:%S.000Z -d "-8 hours"`
  #timestamp=`date +%Y-%m-%dT%H:%M:%S.000Z`
  HostMachineName=`echo "${reconstructionJson}"|grep HostMachineName|awk -F '"' '{print $4}'`
  ProcessName=`echo "${reconstructionJson}"|grep ReleaseName|awk -F '"' '{print $4}'`
  EndTime=`echo "${reconstructionJson}"|grep EndTime|awk -F '"' '{print $4}'`
  #EndTime=`echo "${reconstructionJson}"|grep EndTime|awk -F '"' '{print $4}'|sed 's/Z/000+08:00/g'`
  State=`echo "${reconstructionJson}"|grep State|awk -F '"' '{print $4}'`

  PUT_BODY="{
  \"@timestamp\":\"${EndTime}\",
  \"HostMachineName\":\"${HostMachineName}\",
  \"ProcessName\":\"${ProcessName}\",
  \"State\":\"${State}\"
}"

  #echo ${PUT_BODY} >> test2.log





  curl -X POST ${ESpath}/${indexName}/logEvent -H "Content-Type: application/json" -d "${PUT_BODY}"

  count=$((count+${filterData_foot}))
  sed -i 1,${filterData_foot}d ${tempPath}Jobs_Get_filterData
done

echo > ${tempPath}Jobs_Get_filterData
