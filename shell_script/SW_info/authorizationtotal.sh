#!/bin/bash

#parameter
TokenPath="https://oct1/api/Account/Authenticate"
UserName="\"admin\""
password="\"p@ssw0rd\""
ESpath="http://172.16.97.65:9200"
indexName="authoriznum"
tempPath="/root/you/authorizationsNum/"
Nowtime=`date -d '480 minute ago' +%Y-%m-%dT%H:%M:%S.000Z`


# DELETE ES Data by query
curl -X POST "${ESpath}/${indexName}/_delete_by_query" -H "Content-Type: application/json" -d '{ "query":{ "match":{ "_type":"logEvent" } } }'

#get data
GetToken=`curl -k -X POST ${TokenPath} -H "accept: application/json" -H "Content-Type: application/json" -d '{ "tenancyName": "Default", "usernameOrEmailAddress":'"${UserName}"', "password":'"${password}"'}'| awk -F '"result":"' '{print $2}'|awk -F '","' '{print $1}'`
GetRawdata=`curl -k -X GET "https://oct1/odata/Settings/UiPath.Server.Configuration.OData.GetLicense" -H "accept: application/json" -H "Authorization: Bearer ${GetToken}"`

echo ${GetRawdata} > ${tempPath}rawData
TotalAut=`cat ${tempPath}rawData |awk -F '"Allowed":{' '{print $2}'|awk -F '},' '{print $1}'|sed 's/,/\n/g'|sed '/ABBYY/d'|sed '/DU-SRV/d'|awk -F ':' '{print $2}' | awk '{sum += $1} END {print sum}'`
UseAut=`cat ${tempPath}rawData |awk -F '"Used":{' '{print $2}'|awk -F '},' '{print $1}'|sed 's/,/\n/g'|sed '/ABBYY/d'|sed '/DU-SRV/d'|awk -F ':' '{print $2}' | awk '{sum += $1} END {print sum}'`

percentNum=`echo "$UseAut*100/$TotalAut"| bc`

#echo ${percentNum}

PUT_BODY=""

PUT_BODY="{
  \"@timestamp\":\"${Nowtime}\",
  \"TotalAuthorizationsNum\":\"${TotalAut}\",
  \"UseAuthorizationsNum\":\"${UseAut}\",
  \"percentNum\":\"${percentNum}\"
}"


curl -X POST ${ESpath}/${indexName}/logEvent -H "Content-Type: application/json" -d "${PUT_BODY}"

