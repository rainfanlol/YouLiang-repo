#!/bin/bash

#parameter
TokenPath="https://oct1/api/Account/Authenticate"
UserName="\"admin\""
password="\"p@ssw0rd\""
ESpath="http://172.16.97.65:9200"
indexName="processesorgandname"
tempPath="/root/you/ProcessesUseandTotal/ProcessesOrgandName/"

GetToken=`curl -k -X POST ${TokenPath} -H "accept: application/json" -H "Content-Type: application/json" -d '{ "tenancyName": "Default", "usernameOrEmailAddress":'"${UserName}"', "password":'"${password}"'}'| awk -F '"result":"' '{print $2}'|awk -F '","' '{print $1}'`

GetRawdata=`curl -k -X GET "https://oct1/odata/Releases?%24select=Name%2CJobPriority%2COrganizationUnitFullyQualifiedName" -H "accept: application/json" -H "Authorization: Bearer ${GetToken}"`

echo "${GetRawdata}"|python -m json.tool > ${tempPath}Jobs_Get_JsonData

cat ${tempPath}Jobs_Get_JsonData |grep '"JobPriority": "\|"Name": "\|"OrganizationUnitFullyQualifiedName": "\|\ },'|sed 's/\ },/---------/g'|tr -d ' '|sed 's/OrganizationUnitFullyQualifiedName/Organization/g' > ${tempPath}Jobs_Get_filterData
echo "---------" >> ${tempPath}Jobs_Get_filterData
#cat ${tempPath}Jobs_Get_filterData > test1.log


# DELETE ES Data by query
curl -X POST "${ESpath}/${indexName}/_delete_by_query" -H "Content-Type: application/json" -d '{ "query":{ "match":{ "_type":"logEvent" } } }'


filterData_row=`cat ${tempPath}Jobs_Get_filterData|wc -l`
reconstructionJson=""
PUT_BODY=""
count=1

while [ ${count} -le ${filterData_row} ]
do

  filterData_head=`cat ${tempPath}Jobs_Get_filterData|grep -n JobPriority|head -n 1|awk -F ':' '{print $1}'`
  filterData_foot=`cat ${tempPath}Jobs_Get_filterData|grep -n "\-\-\-\-\-\-\-\-\-"|head -n 1|awk -F ':' '{print $1}'`
  if [ -z ${filterData_head} ] || [ -z ${filterData_foot} ];then
    exit 0
  else
    reconstructionJson=`cat ${tempPath}Jobs_Get_filterData|sed -n ${filterData_head},${filterData_foot}p`
  fi
  #HostMachineName=`echo "${reconstructionJson}"|grep HostMachineName|awk -F '"' '{print $4}'`
  #ProcessName=`echo "${reconstructionJson}"|grep ReleaseName|awk -F '"' '{print $4}'`
  Nowtime=`date -d '480 minute ago' +%Y-%m-%dT%H:%M:%S.000Z`
  ProcessesName=`echo "${reconstructionJson}"|grep Name|awk -F '"' '{print $4}'`
  JobPriority=`echo "${reconstructionJson}"|grep JobPriority|awk -F '"' '{print $4}'`
  Organization=`echo "${reconstructionJson}"|grep Organization|awk -F '"' '{print $4}'`
  #EndTime=`echo "${reconstructionJson}"|grep EndTime|awk -F '"' '{print $4}'|sed 's/Z/000+08:00/g'`
  #State=`echo "${reconstructionJson}"|grep State|awk -F '"' '{print $4}'`

  PUT_BODY="{
  \"@timestamp\":\"${Nowtime}\",
  \"Processesname\":\"${ProcessesName}\",
  \"JobPriority\":\"${JobPriority}\",
  \"OrganizationName\":\"${Organization}\"
}"
  echo $PUT_BODY >> ${tempPath}test.log


  curl -X POST ${ESpath}/${indexName}/logEvent -H "Content-Type: application/json" -d "${PUT_BODY}"

  count=$((count+${filterData_foot}))
  sed -i 1,${filterData_foot}d ${tempPath}Jobs_Get_filterData
done




