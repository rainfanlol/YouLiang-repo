#!/bin/bash

#parameter
TokenPath="https://oct1/api/Account/Authenticate"
UserName="\"admin\""
password="\"p@ssw0rd\""
ESpath="http://172.16.97.65:9200"
indexName="machinesuse"
tempPath="/root/you/Machinesuse/"

GetToken=`curl -k -X POST ${TokenPath} -H "accept: application/json" -H "Content-Type: application/json" -d '{ "tenancyName": "Default", "usernameOrEmailAddress":'"${UserName}"', "password":'"${password}"'}'| awk -F '"result":"' '{print $2}'|awk -F '","' '{print $1}'`

GetRawdata=`curl -k -X GET "https://oct1/odata/Jobs?%24filter=State%20eq%20'Running'" -H "accept: application/json" -H "Authorization: Bearer ${GetToken}"`

#oneTEL
echo "${GetRawdata}"|python -m json.tool > ${tempPath}Jobs_Get_JsonData

cat ${tempPath}Jobs_Get_JsonData |grep '"HostMachineName": *\|\ },'|sed 's/\ },//g'|tr -d ' '|sed '/^$/d'|awk -F ':' '{print $2}'|sed 's/"//g'|sed 's/,//g' > ${tempPath}Jobs_Get_filterid

# DELETE ES Data by query
curl -X POST "${ESpath}/${indexName}/_delete_by_query" -H "Content-Type: application/json" -d '{ "query":{ "match":{ "_type":"logEvent" } } }'

#結果寫入陣列
mapfile listSRobottotal < ${tempPath}Jobs_Get_filterid
#去重
len=${#listSRobottotal[@]}
for((i=0;i<$len;i++))
do
for((j=$len-1;j>i;j--))
do
if [[ ${listSRobottotal[i]} = ${listSRobottotal[j]} ]];then
unset listSRobottotal[i]
fi
done
done



PUT_BODY=""
Nowtime=`date -d '480 minute ago' +%Y-%m-%dT%H:%M:%S.000Z`

#陣列總數
finalNum=`echo ${#listSRobottotal[@]}`

echo ${finalNum}

PUT_BODY="{
  \"@timestamp\":\"${Nowtime}\",
  \"TotalMachinesNumber\":\"${finalNum}\"
}"


curl -X POST ${ESpath}/${indexName}/logEvent -H "Content-Type: application/json" -d "${PUT_BODY}"

#echo > /root/you/testcom/Get_totalRobotNum
#echo > /root/you/testcom/Jobs_Get_filterNum

