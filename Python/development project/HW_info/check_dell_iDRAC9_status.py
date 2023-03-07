#!/usr/bin/python3
# -*- coding: UTF-8 -*-


from function_you.function_inputfunction import *
from function_you.function_dataTime import *
from function_you.function_icinga import *
from function_you.function_insert_mysql import function_query_mysql
from function_you.function_ospopen import function_ospopen
from function_you.function_checkstatus import *
from function_you.function_DataFrameToSql import *



### 命令行輸入參數 ###
command = sys.argv
version = command[1]
community = command[2]
HostIP = command[3] #snmp_address
port = command[4]
host_address = command[5]
#Warning_water_level = command[5]
#Critical_water_level = command[6]
#Ok_water_level = command[7]

### 自定義變數  ###
global MibDir
MibDir = "IDRAC-MIB-SMIv2"
global apiname
apiname = "HWinfoByiDRAC9"
global tablename 
tablename = "mirle_mon_Server_DELL"



par = [version,community,HostIP,port]

###自訂函數
def CM(n1):
  result = os.popen("snmpwalk -M +/usr/share/snmp/servicedj-mibs/dell-mibs/ -m "+MibDir+" -v "+par[0]+" -c "+par[1]+" "+par[2]+":"+par[3]+" "+n1).read()
  return result
def CMN(n2):
  result = os.popen("snmpwalk -Oqv -M +/usr/share/snmp/servicedj-mibs/dell-mibs/ -m "+MibDir+" -v "+par[0]+" -c "+par[1]+" "+par[2]+":"+par[3]+" "+n2).read()
  return result

### 定義OBJ和NAME變數  ###
#displayname = function_icinga_displayname(host_address)
#objectid = function_icinga_objectid(host_address,displayname)
displayname = function_icinga_displayname(host_address)
objectid = function_icinga_objectid(host_address,displayname)
#displayname = 123
#objectid = 456

###當exit 1觸發此函數###
#def SendErrorMessage():
# print(function_getDataTime()" "HostIP" "displayname":happen warning or critical")
# return

### 主程式  ###

def main() :

### dataframe行列全顯示  ###
 pd.set_option('display.max_columns', None)
 pd.set_option('display.max_rows', None)

### status處理變數
 firs = """ | sed 's/ok/0/g' | sed 's/nonCritical/1/g' | sed 's/other/2/g' | sed 's/unknown/3/g' | sed 's/critical/2/g' | sed 's/nonRecoverable/2/g' | sed 's/"//g'"""
 secs = """ | sed 's/ok/0/g' | sed 's/nonCriticalUpper/1/g' | sed 's/nonCriticalLower/1/g' | sed 's/other/2/g' | sed 's/unknown/3/g' | sed 's/criticalUpper/2/g' | sed 's/nonRecoverableUpper/2/g' | sed 's/criticalLower/2/g' | sed 's/nonRecoverableLower/2/g' | sed 's/failed/2/g' | sed 's/"//g'"""
 tri = """ | sed 's/"//g'"""
###cpu
 ###key
 cpukey=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.32.1.7"""+tri).strip().split("\n")
 ###value
 cpuvalues=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.30.1.5"""+tri).strip().split("\n")
 ###status
 cpuvalue=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.30.1.5"""+firs).strip().split("\n")

###memory
 ###key
 memkey=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.50.1.8"""+tri).strip().split("\n")
 ###value
 memvalues=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.50.1.5"""+tri).strip().split("\n")
 ###status
 memvalue=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.50.1.5"""+firs).strip().split("\n")

###Fan
 ###key
 fankey=CMN(""".1.3.6.1.4.1.674.10892.5.4.700.12.1.8"""+tri).strip().split("\n")
 ###value
 fanvalues=CMN(""".1.3.6.1.4.1.674.10892.5.4.700.12.1.5"""+tri).strip().split("\n")
 ###status
 fanvalue=CMN(""".1.3.6.1.4.1.674.10892.5.4.700.12.1.5"""+secs).strip().split("\n")

###power
 ###key
 psukey=CMN(""".1.3.6.1.4.1.674.10892.5.4.600.12.1.8"""+tri).strip().split("\n")
 ###value
 psuvalues=CMN(""".1.3.6.1.4.1.674.10892.5.4.600.12.1.5"""+tri).strip().split("\n")
 ###status
 psuvalue=CMN(""".1.3.6.1.4.1.674.10892.5.4.600.12.1.5"""+firs).strip().split("\n")

###nic
 ###key
 nickey=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.90.1.6"""+tri).strip().split("\n")
 ###value
 nicvalues=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.90.1.3"""+tri).strip().split("\n")
 ###status
 nicvalue=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.90.1.3"""+firs).strip().split("\n")

###disk
 ###key
 diskkey=CMN(""".1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.2"""+tri).strip().split("\n")
 ###value
 diskvalues=CMN(""".1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.24"""+tri).strip().split("\n")
 ###status
 diskvalue=CMN(""".1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.24"""+firs).strip().split("\n")

###virtualdisk
 ###key
 virkey=CMN(""".1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.36"""+tri).strip().split("\n")
 ###value
 virvalues=CMN(""".1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.20"""+tri).strip().split("\n")
 ###status
 virvalue=CMN(""".1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.20"""+firs).strip().split("\n")

###battery
 ###key
 batkey=CMN(""".1.3.6.1.4.1.674.10892.5.4.600.50.1.7"""+tri).strip().split("\n")
 ###value
 batvalues=CMN(""".1.3.6.1.4.1.674.10892.5.4.600.50.1.5"""+tri).strip().split("\n")
 ###status
 batvalue=CMN(""".1.3.6.1.4.1.674.10892.5.4.600.50.1.5"""+firs).strip().split("\n")

###pci
 ###key
 pcikey=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.80.1.9"""+tri).strip().split("\n")
 ###value
 pcivalues=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.80.1.5"""+tri).strip().split("\n")
 ###status
 pcivalue=CMN(""".1.3.6.1.4.1.674.10892.5.4.1100.80.1.5"""+firs).strip().split("\n")

###enclosure
 ###key
 enckey=CMN(""".1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.2"""+tri).strip().split("\n")
 ###value
 encvalues=CMN(""".1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.24"""+tri).strip().split("\n")
 ###status
 encvalue=CMN(""".1.3.6.1.4.1.674.10892.5.5.1.20.130.3.1.24"""+firs).strip().split("\n")

###keytitle欄位處理
 titlekeylist=["零件名稱","CPU","Memory","Fan","PowerSupply","NIC","LocalStorage","Virtualdisk","CacheBattery","PCI","enclosure"]
 keylist=cpukey+memkey+fankey+psukey+nickey+diskkey+virkey+batkey+pcikey+enckey
 allkeylist=keylist+titlekeylist
# print(len(keylist))
###status處理
 titlelist=[cpuvalue,memvalue,fanvalue,psuvalue,nicvalue,diskvalue,virvalue,batvalue,pcivalue,encvalue]
 tilist=[0]
 for i in range(len(titlelist)):
   tilist.append(TitleStatus(titlelist[i]))

 statuslist=cpuvalue+memvalue+fanvalue+psuvalue+nicvalue+diskvalue+virvalue+batvalue+pcivalue+encvalue
# print(len(statuslist))
 allstatuslist=statuslist+tilist
 allvaluelist=cpuvalues+memvalues+fanvalues+psuvalues+nicvalues+diskvalues+virvalues+batvalues+pcivalues+encvalues+tilist

 intallstatuslist=[int(i) for i in allstatuslist]

###12/14告警格式
 alerttitle=[]
# print(statuslist)
 statuslist=list(map(int,statuslist))
 for j in range(len(statuslist)):
  if statuslist[j] == 2:
    alerttitle.append(f"[critical]{keylist[j]}=2")
  elif statuslist[j] == 1:
    alerttitle.append(f"[warning]{keylist[j]}=1")
  elif statuslist[j] == 3:
    alerttitle.append(f"[unknown]{keylist[j]}=3")
  else:
    continue
 print(*alerttitle, sep=';')
###告警訊息內容與狀態判斷(整體零件狀況判斷)
 allstatus=TitleStatus(tilist)
 allstatus=int(allstatus)
# if allstatus == 0:
#  print (f"時間:{function_getDataTime()} IP:{HostIP} 設備名稱:{displayname} 目前設備狀態:OK")
# elif allstatus == 1:
#  print (f"時間:{function_getDataTime()} IP:{HostIP} 設備名稱:{displayname} 目前設備狀態:Warning")
# elif allstatus == 2:
#  print (f"時間:{function_getDataTime()} IP:{HostIP} 設備名稱:{displayname} 目前設備狀態:Critical")
# else :
#  print (f"時間:{function_getDataTime()} IP:{HostIP} 設備名稱:{displayname} 目前設備狀態:Unknown")


###layer處理
 layerlist=[cpuvalue,memvalue,fanvalue,psuvalue,nicvalue,diskvalue,virvalue,batvalue,pcivalue,encvalue]
 halflayer=list()
 for i in range(0, 10):
  for  j in range(len(layerlist[i])):
   halflayer.append(str(i+1)+','+str(j+1))

 titlelayerlist=["0","1","2","3","4","5","6","7","8","9","10"]
 alllayerlist=halflayer+titlelayerlist

###value處理
 tivaluelist=[0]
 tempvaluelist=[]

 valuelisthand=[cpuvalues,memvalues,fanvalues,psuvalues,nicvalues,diskvalues,virvalues,batvalues,pcivalues,encvalues]
 cut = ';'
 for i in range(len(valuelisthand)):
  listonly = list(set(valuelisthand[i]))
  listonly.sort(key=valuelisthand[i].index)
  for j in listonly:
   valuefstring=f"{valuelisthand[i].count(j)} {j}"
   tempvaluelist.append(valuefstring)
  onevalue=f"{cut.join(tempvaluelist)}"
  tivaluelist.append(onevalue)
  del onevalue
  del tempvaluelist
  tempvaluelist=[]
# print(tivaluelist)
 allvaluelist=cpuvalues+memvalues+fanvalues+psuvalues+nicvalues+diskvalues+virvalues+batvalues+pcivalues+encvalues+tivaluelist

 ###宣告其餘欄位空list
 objid, devicename, apinamelist, inserdate= ([] for i in range(4))

 ###剛宣告list
 for i in range(len(allkeylist)):
  objid.append(objectid)
  devicename.append(displayname)
  apinamelist.append(apiname)
  inserdate.append(function_getDataTime())

 ###list轉df
 dictionary={'icin_host_object_id':{},'Device':{},'APIname':{},'dataKey':{},'dataValue':{},'status':{},'layer':{},'insert_date':{}}
 dataframe=pd.DataFrame(dictionary)
 dataframe['icin_host_object_id']=objid
 dataframe['Device']=devicename
 dataframe['APIname']=apinamelist
 dataframe['dataKey']=allkeylist
 dataframe['dataValue']=allvaluelist
 dataframe['status']=intallstatuslist
 dataframe['layer']=alllayerlist
 dataframe['insert_date']=inserdate

 dataframe.loc[dataframe.layer=='0','dataValue']="""狀態"""
 print("----- Raw Data -----")
 print("Dataframe=\n",dataframe)
 delsql=f"delete from {tablename} WHERE icin_host_object_id = {objectid} and Device = '{displayname}' and APIname = '{apiname}'"
 temptime=function_getDataTime()
 uptimesql=f"UPDATE {tablename} SET insert_date = \"{temptime}\""
 DataFrameToSqll(dataframe,delsql,uptimesql,tablename)
# print("Data transferred from dataframe to mysql successfully")

 sys.exit(allstatus)
 #end

if __name__ == '__main__':
  main()
