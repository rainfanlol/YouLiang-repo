#!/bin/bash

#parameter
TokenPath="https://oct1/api/Account/Authenticate"
UserName="\"admin\""
password="\"p@ssw0rd\""
Nowtime=`date -d '8 hours ago' +%Y-%m-%dT%H:%M:%S.000Z`
timestamp=`date +%Y-%m-%dT%H:%M:%S.000Z`
ESpath="http://172.16.97.65:9200"
indexName="machinesusedetails"
tempPath="/root/you/MachinesUseandTotal/MachinesUseDetail/"



GetToken=`curl -k -X POST ${TokenPath} -H "accept: application/json" -H "Content-Type: application/json" -d '{ "tenancyName": "Default", "usernameOrEmailAddress":'"${UserName}"', "password":'"${password}"'}'| awk -F '"result":"' '{print $2}'|awk -F '","' '{print $1}'`


GetRawdata=`curl -k -X GET "https://oct1/odata/Machines?%24select=Name" -H "accept: application/json" -H "Authorization: Bearer ${GetToken}"`

echo ${GetRawdata}|python -m json.tool > ${tempPath}Jobs_Get_rawData1012
cat ${tempPath}Jobs_Get_rawData1012 |grep '"Name": "\|\ },'|sed 's/\ },/---------/g' |sed '/---------/d' |awk -F ':' '{print $2}'|sed 's/"//g'|tr -d ' '> ${tempPath}Jobs_Get_filterData

GetRawdata2=`curl -k -X GET "https://oct1/odata/Jobs?%24filter=State%20ne%20'Successful'%20and%20State%20ne%20'Faulted'%20and%20State%20ne%20'Stopped'&%24select=HostMachineName%2CReleaseName%2CState" -H "accept: application/json" -H "Authorization: Bearer ${GetToken}"`

echo ${GetRawdata2}|python -m json.tool > ${tempPath}Jobs_Get_JsonData

i=0
array=
while read LINE
do
    array[$i]=$LINE
    ((i += 1))
done < ${tempPath}Jobs_Get_filterData

#刪資料
curl -X POST "${ESpath}/${indexName}/_delete_by_query" -H "Content-Type: application/json" -d '{ "query":{ "match":{ "_type":"logEvent" } } }'


for item in ${array[@]};do
     strA=`cat ${tempPath}Jobs_Get_JsonData`
     strB="$item"
     if [[ $strA =~ $strB ]]
      then
       continue
      else
       PUT_BODY="{
       \"@timestamp\":\"${Nowtime}\",
       \"MachineName\":\"${item}\",
       \"Processesname\":\"None\",
       \"State\":\"Available\"
 }"
       curl -X POST ${ESpath}/${indexName}/logEvent -H "Content-Type: application/json" -d "${PUT_BODY}"
     fi
done

cat ${tempPath}Jobs_Get_JsonData >> ${tempPath}test10132.log
cat ${tempPath}Jobs_Get_JsonData |grep '"State": "\|"ReleaseName": "\|"HostMachineName": "\|\ },'|sed 's/\ },/---------/g'|tr -d ' '|sed 's/ReleaseName/processesname/g' > ${tempPath}Jobs_Get_filterData2
echo "---------" >> ${tempPath}Jobs_Get_filterData2
#cat ${tempPath}Jobs_Get_filterData2 >> ${tempPath}test1013.log
filterData_row=`cat ${tempPath}Jobs_Get_filterData2|wc -l`
reconstructionJson=""
PUT_BODY=""
count=1

while [ ${count} -le ${filterData_row} ]
do

  filterData_head=`cat ${tempPath}Jobs_Get_filterData2|grep -n HostMachineName|head -n 1|awk -F ':' '{print $1}'`
  filterData_foot=`cat ${tempPath}Jobs_Get_filterData2|grep -n "\-\-\-\-\-\-\-\-\-"|head -n 1|awk -F ':' '{print $1}'`
  if [ -z ${filterData_head} ] || [ -z ${filterData_foot} ];then
    exit 0
  else
    reconstructionJson=`cat ${tempPath}Jobs_Get_filterData2|sed -n ${filterData_head},${filterData_foot}p`
    echo ${reconstructionJson} >> ${tempPath}tests.log
  fi
  HostMachineName=`echo "${reconstructionJson}"|grep HostMachineName|awk -F '"' '{print $4}'`
  ProcessesName=`echo "${reconstructionJson}"|grep processesname|awk -F '"' '{print $4}'`
  State=`echo "${reconstructionJson}"|grep State|awk -F '"' '{print $4}'`

  PUT_BODY="{
  \"@timestamp\":\"${Nowtime}\",
  \"MachineName\":\"${HostMachineName}\",
  \"Processesname\":\"${ProcessesName}\",
  \"State\":\"${State}\"
}"


  curl -X POST ${ESpath}/${indexName}/logEvent -H "Content-Type: application/json" -d "${PUT_BODY}"

  count=$((count+${filterData_foot}))
  sed -i 1,${filterData_foot}d ${tempPath}Jobs_Get_filterData2
done





