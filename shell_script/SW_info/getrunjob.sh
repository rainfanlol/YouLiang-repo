#!/bin/bash

#parameter
TokenPath="https://oct1/api/Account/Authenticate"
UserName="\"admin\""
password="\"p@ssw0rd\""
LastDay=`date -d last-day +%Y-%m-%d`
#Nowtime=`date +%Y-%m-%d`
Nowtime=`date -d '480 minute ago' +%Y-%m-%dT%H`
NowtimeMin=`date -d '480 minute ago' +%M`
NowtimeSec=`date -d '480 minute ago' +%S`
timestamp=`date +%Y-%m-%dT%H:%M:%S.000Z`
ESpath="http://172.16.97.65:9200"
indexName="test0911"



GetToken=`curl -k -X POST ${TokenPath} -H "accept: application/json" -H "Content-Type: application/json" -d '{ "tenancyName": "Default", "usernameOrEmailAddress":'"${UserName}"', "password":'"${password}"'}'| awk -F '"result":"' '{print $2}'|awk -F '","' '{print $1}'`

GetRawdata=`curl -k -X GET "https://oct1/odata/Jobs?%24filter=CreationTime%20gt%20${LastDay}T00%3A00%3A00.000Z%20and%20CreationTime%20lt%20${Nowtime}%3A${NowtimeMin}%3A${NowtimeSec}.000Z" -H "accept: application/json" -H "Authorization: Bearer ${GetToken}"`


echo "${GetRawdata}"|python -m json.tool > Jobs_Get_rawData
cat Jobs_Get_rawData |grep '"CreationTime": "\|"HostMachineName": "\|"ReleaseName": "\|"StartTime": "\|"EndTime": "\|"State": "\|\ },'|sed 's/\ },/---------/g'|tr -d ' ' > Jobs_Get_filterData
echo "---------" >> Jobs_Get_filterData

filterData_row=`cat Jobs_Get_filterData|wc -l`
reconstructionJson=""
PUT_BODY=""
count=1


# DELETE ES Data by query
curl -X POST "${ESpath}/${indexName}/_delete_by_query" -H "Content-Type: application/json" -d '{ "query":{ "match":{ "_type":"logEvent" } } }'


while [ ${count} -le ${filterData_row} ]
do

  filterData_head=`cat Jobs_Get_filterData|grep -n CreationTime|head -n 1|awk -F ':' '{print $1}'`
  filterData_foot=`cat Jobs_Get_filterData|grep -n "\-\-\-\-\-\-\-\-\-"|head -n 1|awk -F ':' '{print $1}'`
  if [ -z ${filterData_head} ] || [ -z ${filterData_foot} ];then
    exit 0
  else
    reconstructionJson=`cat Jobs_Get_filterData|sed -n ${filterData_head},${filterData_foot}p`
  fi

  #timestamp=`date +%Y-%m-%dT%H:%M:%S.000Z -d "-8 hours"`
  #timestamp=`date +%Y-%m-%dT%H:%M:%S.000Z`
  HostMachineName=`echo "${reconstructionJson}"|grep HostMachineName|awk -F '"' '{print $4}'`
  ProcessName=`echo "${reconstructionJson}"|grep ReleaseName|awk -F '"' '{print $4}'`
  #EndTime=`echo "${reconstructionJson}"|grep EndTime|awk -F '"' '{print $4}'`
  CreationTime=`echo "${reconstructionJson}"|grep CreationTime|awk -F '"' '{print $4}'`
  #EndTime=`echo "${reconstructionJson}"|grep EndTime|awk -F '"' '{print $4}'|sed 's/Z/000+08:00/g'`
  State=`echo "${reconstructionJson}"|grep State|awk -F '"' '{print $4}'`

  PUT_BODY="{
  \"@timestamp\":\"${CreationTime}\",
  \"HostMachineName\":\"${HostMachineName}\",
  \"ProcessName\":\"${ProcessName}\",
  \"State\":\"${State}\"
}"







  curl -X POST ${ESpath}/${indexName}/logEvent -H "Content-Type: application/json" -d "${PUT_BODY}"

  count=$((count+${filterData_foot}))
  sed -i 1,${filterData_foot}d Jobs_Get_filterData
done
