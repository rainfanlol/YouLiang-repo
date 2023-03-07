#!/bin/bash

#parameter
TokenPath="https://oct1/api/Account/Authenticate"
UserName="\"admin\""
password="\"p@ssw0rd\""
ESpath="http://172.16.97.65:9200"
indexName="authoriznumuse"
#indexName="test1013"
tempPath="/root/you/authorizationsNum/authorizationDetail/"
Nowtime=`date -d '480 minute ago' +%Y-%m-%dT%H:%M:%S.000Z`


# DELETE ES Data by query
curl -X POST "${ESpath}/${indexName}/_delete_by_query" -H "Content-Type: application/json" -d '{ "query":{ "match":{ "_type":"logEvent" } } }'

#get data
GetToken=`curl -k -X POST ${TokenPath} -H "accept: application/json" -H "Content-Type: application/json" -d '{ "tenancyName": "Default", "usernameOrEmailAddress":'"${UserName}"', "password":'"${password}"'}'| awk -F '"result":"' '{print $2}'|awk -F '","' '{print $1}'`
GetRawdata=`curl -k -X GET "https://oct1/odata/Settings/UiPath.Server.Configuration.OData.GetLicense" -H "accept: application/json" -H "Authorization: Bearer ${GetToken}"`

echo ${GetRawdata} > ${tempPath}rawData
#echo ${GetRawdata}|python -m json.tool > ${tempPath}rawData
TotalAut=`cat ${tempPath}rawData |awk -F '"Allowed":{' '{print $2}'|awk -F '},' '{print $1}'|sed 's/,/\n/g'|sed '/ABBYY/d'|sed '/DU-SRV/d'|sed '/Headless/d'|sed 's/"//g'`
#TotalAut=`cat ${tempPath}rawData |awk -F '"Allowed":{' '{print $2}'|awk -F '},' '{print $1}'|sed 's/,/\n/g'|sed '/ABBYY/d'|sed '/DU-SRV/d'|awk -F ':' '{print $2}' | awk '{sum += $1} END {print sum}'`
UseAut=`cat ${tempPath}rawData |awk -F '"Used":{' '{print $2}'|awk -F '},' '{print $1}'|sed 's/,/\n/g'|sed '/ABBYY/d'|sed '/DU-SRV/d'|sed '/Headless/d'|sed 's/"//g'`

echo "${TotalAut}" > ${tempPath}total.log
echo "${UseAut}" > ${tempPath}use.log

#percentNum=`echo "$UseAut*100/$TotalAut"| bc`
#ProcessName=`echo "${reconstructionJson}"|grep ReleaseName|awk -F '"' '{print $4}'`
Developmentuse=`cat ${tempPath}use.log|grep Development |awk -F ':' '{print $2}'`
StudioXues=`cat ${tempPath}use.log|grep StudioX|awk -F ':' '{print $2}'`
StudioProuse=`cat ${tempPath}use.log|grep StudioPro|awk -F ':' '{print $2}'`
Attendeduse=`cat ${tempPath}use.log|grep Attended|awk -F ':' '{print $2}'`
NonProductionuse=`cat ${tempPath}use.log|grep NonProduction|awk -F ':' '{print $2}'`
TestAutomationuse=`cat ${tempPath}use.log|grep TestAutomation|awk -F ':' '{print $2}'`
Unattendeduse=`cat ${tempPath}use.log|grep Unattended|awk -F ':' '{print $2}'`

Developmenttotal=`cat ${tempPath}total.log|grep Development |awk -F ':' '{print $2}'`
StudioXtotal=`cat ${tempPath}total.log|grep StudioX|awk -F ':' '{print $2}'`
StudioPrototal=`cat ${tempPath}total.log|grep StudioPro|awk -F ':' '{print $2}'`
Attendedtotal=`cat ${tempPath}total.log|grep Attended|awk -F ':' '{print $2}'`
NonProductiontotal=`cat ${tempPath}total.log|grep NonProduction|awk -F ':' '{print $2}'`
TestAutomationtotal=`cat ${tempPath}total.log|grep TestAutomation|awk -F ':' '{print $2}'`
Unattendedtotal=`cat ${tempPath}total.log|grep Unattended|awk -F ':' '{print $2}'`

Developmentper=`echo "$Developmentuse*100/$Developmenttotal"| bc`
StudioXper=`echo "$StudioXues*100/$StudioXtotal"| bc`
StudioProper=`echo "$StudioProuse*100/$StudioPrototal"| bc`
Attendedper=`echo "$Attendeduse*100/$Attendedtotal"| bc`
NonProductionper=`echo "$NonProductionuse*100/$NonProductiontotal"| bc`
TestAutomationper=`echo "$TestAutomationuse*100/$TestAutomationtotal"| bc`
Unattendedper=`echo "$Unattendeduse*100/$Unattendedtotal"| bc`


PUT_BODY=""

PUT_BODY="{
  \"@timestamp\":\"${Nowtime}\",
  \"Developmentuse\":\"${Developmentuse}\",
  \"StudioXues\":\"${StudioXues}\",
  \"StudioProuse\":\"${StudioProuse}\",
  \"Attendeduse\":\"${Attendeduse}\",
  \"NonProductionuse\":\"${NonProductionuse}\",
  \"TestAutomationuse\":\"${TestAutomationuse}\",
  \"Unattendeduse\":\"${Unattendeduse}\",
  \"Developmenttotal\":\"${Developmenttotal}\",
  \"StudioXtotal\":\"${StudioXtotal}\",
  \"StudioPrototal\":\"${StudioPrototal}\",
  \"Attendedtotal\":\"${Attendedtotal}\",
  \"NonProductiontotal\":\"${NonProductiontotal}\",
  \"TestAutomationtotal\":\"${TestAutomationtotal}\",
  \"Unattendedtotal\":\"${Unattendedtotal}\",
  \"Developmentper\":\"${Developmentper}\",
  \"StudioXper\":\"${StudioXper}\",
  \"StudioProper\":\"${StudioProper}\",
  \"Attendedper\":\"${Attendedper}\",
  \"NonProductionper\":\"${NonProductionper}\",
  \"TestAutomationper\":\"${TestAutomationper}\",
  \"Unattendedper\":\"${Unattendedper}\"
}"

#echo ${PUT_BODY}
curl -X POST ${ESpath}/${indexName}/logEvent -H "Content-Type: application/json" -d "${PUT_BODY}"

