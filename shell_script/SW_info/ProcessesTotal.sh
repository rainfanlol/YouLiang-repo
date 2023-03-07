#!/bin/bash

#parameter
TokenPath="https://oct1/api/Account/Authenticate"
UserName="\"admin\""
password="\"p@ssw0rd\""
#Nowtime=`date +%Y-%m-%d`
Nowtime=`date -d '480 minute ago' +%Y-%m-%dT%H`
NowtimeMin=`date -d '480 minute ago' +%M`
NowtimeSec=`date -d '480 minute ago' +%S`
OneHourtime=`date -d '960 minute ago' +%Y-%m-%dT%H`
OneHourtimeMin=`date -d '960 minute ago' +%M`
OneHourtimeSec=`date -d '960 minute ago' +%S`
timestamp=`date -d '480 minute ago' +%Y-%m-%dT%H:%M:%S.000Z`
ESpath="http://172.16.97.65:9200"
indexName="processestotal"
tempPath="/root/you/ProcessesTotal/"


GetToken=`curl -k -X POST ${TokenPath} -H "accept: application/json" -H "Content-Type: application/json" -d '{ "tenancyName": "Default", "usernameOrEmailAddress":'"${UserName}"', "password":'"${password}"'}'| awk -F '"result":"' '{print $2}'|awk -F '","' '{print $1}'`

GetRawdata=`curl -k -X GET "https://oct1/odata/Processes" -H "accept: application/json" -H "Authorization: Bearer ${GetToken}"`

#echo ${GetRawdata} > ${tempPath}test.log

echo "${GetRawdata}"|python -m json.tool > ${tempPath}Jobs_Get_rawData
cat ${tempPath}Jobs_Get_rawData |awk -F '"@odata.count":' '{print $2}' |awk -F ',' '{print $1}'|tr -d ' '|sed '/^$/d' > ${tempPath}Jobs_Get_filterData
#echo "---------" >> ${tempPath}Jobs_Get_filterData

#filterData_row=`cat ${tempPath}Jobs_Get_filterData|wc -l`
reconstructionJson=""
PUT_BODY=""
count=1


# DELETE ES Data by query
curl -X POST "${ESpath}/${indexName}/_delete_by_query" -H "Content-Type: application/json" -d '{ "query":{ "match":{ "_type":"logEvent" } } }'

totalnum=`cat ${tempPath}Jobs_Get_filterData`

PUT_BODY="{
  \"@timestamp\":\"${timestamp}\",
  \"processestotal\":\"${totalnum}\"
}"



curl -X POST ${ESpath}/${indexName}/logEvent -H "Content-Type: application/json" -d "${PUT_BODY}"

echo > ${tempPath}Jobs_Get_filterData
