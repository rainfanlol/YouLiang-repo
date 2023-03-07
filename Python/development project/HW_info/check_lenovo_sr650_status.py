#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#功能:監控lenovo sr650 硬體狀態


### 內部函數 ###
import sys, os, time, re, platform

### 第三方套件函數  ###
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import mysql.connector
from mysql.connector import Error



### 命令行輸入參數 ###
command = sys.argv
version = command[1]
level = command[2]
userid = command[3]
PROTOCOL = command[4]
PASSPHRASE = command[5]
xPROTOCOL = command[6]
xPASSPHRASE = command[7]
hostip = command[8]
port = command[9]
#low_level = command[10]
#high_level = command[11]


### 自定義變數  ###

APIname="HWinfoByLenovoSR650"
par = [version,level,userid,PROTOCOL,PASSPHRASE,xPROTOCOL,xPASSPHRASE,hostip,port]
keylist = ["LENOVO-XCC-MIB::cpuVpdDescription","LENOVO-XCC-MIB::memoryVpdDescription","LENOVO-XCC-MIB::powerFruName","LENOVO-XCC-MIB::diskFruName","LENOVO-XCC-MIB::fanDescr","LENOVO-XCC-MIB::raidCtrlBatBCKProdName","LENOVO-XCC-MIB::voltDescr"]
valuelist = ["LENOVO-XCC-MIB::cpuVpdHealthStatus","LENOVO-XCC-MIB::memoryHealthStatus","LENOVO-XCC-MIB::powerHealthStatus","LENOVO-XCC-MIB::diskHealthStatus","LENOVO-XCC-MIB::fanHealthStatus","LENOVO-XCC-MIB::raidCtrlBatBCKStatus","LENOVO-XCC-MIB::voltHealthStatus","LENOVO-XCC-MIB::systemHealthStat"]

#oidtitle = '.1.3.6.1.4.1.2021.54'
#processoid = ".3.1.2.7.47.98.105.110.47.115.104"



### 自定義函式  ###
def function_getDataTime():
        localDateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return localDateTime

### 找displayname  ###
def function_icinga_displayname(hostip):

        ### default variable
        command = "SELECT icinga_hosts.display_name FROM icinga2.icinga_hosts LEFT JOIN icinga2.icinga_objects ON icinga_hosts.host_object_id = icinga_objects.object_id WHERE icinga_hosts.address = '"+hostip+"' AND icinga_objects.is_active = 1;"
        database = "icinga2"

        ### get dissplayname
        revalue = function_query_mysql(command,database).splitlines()[1]

        ### return
        return revalue

### 找obj id  ###
def function_icinga_objectid(hostip,displayname):

        ### default variable
        command = "SELECT icinga_hosts.host_object_id FROM icinga2.icinga_hosts LEFT JOIN icinga2.icinga_objects ON icinga_hosts.host_object_id = icinga_objects.object_id WHERE icinga_hosts.address = '"+hostip+"' AND icinga_objects.is_active = 1 AND icinga_hosts.display_name = '"+displayname+"';"
        database = "icinga2"

        ### get objectid
        revalue = function_query_mysql(command,database).splitlines()[1]

        ### return
        return revalue

def function_query_mysql(command,database):

        ### query mysql
#       revalue = function_ospopen("sudo mysql --login-path=remote -D %s -e \"%s\"" % (database,command))
        revalue = function_ospopen("sudo mysql -D %s -e \"%s\"" % (database,command))
        ### return value
        return revalue



def function_ospopen(command):

        ###
        osp = os.popen("%s" % command)
        popvalue = osp.read()
        osp.close()

        ### return
        return popvalue

def CM(n1):
                     #字串與變數合成
  result = os.popen("snmpwalk -m LENOVO-XCC-MIB -v "+par[0]+" -l "+par[1]+" "+par[2]+":"+par[3]+" "+oidtitle+""+n1)
  return result

def CMN(n2):
  result = os.popen("snmpwalk -Oqv -m LENOVO-XCC-MIB -v "+par[0]+" -l "+par[1]+" -u "+par[2]+" -a "+par[3]+" -A "+par[4]+" -x "+par[5]+ " -X "+par[6]+" "+par[7]+":"+par[8]+" "+n2+""" | sed 's/"//g' | sed 's/Normal/0/g' | sed 's/NonCritical/1/g' | sed 's/Critical/2/g' | sed 's/NonRecoverable/2/g' | sed 's/normal/0/g' | sed 's/Operational/0/g'""").read()
  return result

def CMNC(n3):
  result = os.popen("snmpwalk -Oqv -m LENOVO-XCC-MIB -v "+par[0]+" -l "+par[1]+" -u "+par[2]+" -a "+par[3]+" -A "+par[4]+" -x "+par[5]+ " -X "+par[6]+" "+par[7]+":"+par[8]+" "+n3+""" | sed 's/"//g'""").read()
  return result


def paa():
  print ('############################################################################################################')

###判斷status函數
def titlestatus(lis):
 result = 0
 for i in range(len(lis)):
  if (lis[i] == 1 ):
     result = 1
     continue
    
  elif (lis[i] == 2 ):
     result = 2
     return result
     break
  else:
     continue
 return result


def DataFrameToSql(dataframe):
 try:
  ### 取得mysql登入相關info ###
  getdbinfo=os.popen("mysql --print-defaults|grep host| sed 's/--//g'").read()
  dbinfo=re.split(' |=',getdbinfo)
  del dbinfo[-1]
  keylist=list()
  valuelist=list()
  for i in range (0,len(dbinfo),2):
   keylist.append(dbinfo[i])

  for j in range (1,len(dbinfo),2):
   valuelist.append(dbinfo[j])
  dbdict = dict(zip(keylist,valuelist))
  ### new connection ###
#  conn=mysql.connector.connect(host="servicedj-mariadb",user="mspadmin",password="MIRLEau4a832019",database="icinga2",charset="utf8")
  conn=mysql.connector.connect(host=dbdict['host'],user=dbdict['user'],password=dbdict['password'],database=dbdict['database'],charset=dbdict['default-character-set'])
  cur=conn.cursor()
  bugnum="'"+hostip+"'"
#  print(bugnum)
  cur.execute("delete from mirle_mon_Server_Lenovo WHERE icin_host_object_id = "+objectid+" and Device = \""+displayname+"\" and APIname = \"HWinfoByLenovoSR650\"")
  conn.commit()
#  cur.close()

  engine = create_engine('mysql+pymysql://'+dbdict['user']+':'+dbdict['password']+'@'+dbdict['host']+':'+dbdict['port']+'/'+dbdict['database'])


  dataframe.to_sql(
      name='mirle_mon_Server_Lenovo',
      con=engine,
      index=False,
      if_exists='append'
  )
  temptime=function_getDataTime()
  cur.execute("UPDATE mirle_mon_Server_Lenovo SET insert_date = \""+temptime+"\"")
  conn.commit()
  cur.close()
 except Error as e:
   print("Error in Mysql connection=",e)
 finally:
   conn.close()

### 定義OBJ和NAME變數  ###
#displayname = 123
#objectid = 456

displayname = function_icinga_displayname(hostip)
objectid = function_icinga_objectid(hostip,displayname)


### 主程式  ###
def main() :

### dataframe行列全顯示  ###
 pd.set_option('display.max_columns', None)
 pd.set_option('display.max_rows', None)

### 函數回傳原始資料格式  ###
###key處理
 cpukey = CMN(keylist[0]).strip().split("\n")
 memkey = CMN(keylist[1]).strip().split("\n")
 powerkey = CMN(keylist[2]).strip().split("\n")
 diskkey = CMN(keylist[3]).strip().split("\n")
 fankey = CMN(keylist[4]).strip().split("\n")
 batkey = CMN(keylist[5]).strip().split("\n")
 votkey = CMN(keylist[6]).strip().split("\n")

 titlekeylist=["零件狀態","CPU","Memory","PowerSupply","LocalStorage","Fan","Battery","Voltage","XCC Module"]
 allkeylist=cpukey+memkey+powerkey+diskkey+fankey+batkey+votkey+titlekeylist
###status資料收集
 cpus = CMN(valuelist[0]).strip().split("\n")
 mems = CMN(valuelist[1]).strip().split("\n")
 powers = CMN(valuelist[2]).strip().split("\n")
 disks = CMN(valuelist[3]).strip().split("\n")
 fans = CMN(valuelist[4]).strip().split("\n")
 bats = CMN(valuelist[5]).strip().split("\n")
 vots = CMN(valuelist[6]).strip().split("\n")
 syss = CMN(valuelist[7]).strip().split("\n")

###status處理
 titlelist=[cpus,mems,powers,disks,fans,bats,vots,syss]
 tilist=[0]
 for i in range(len(titlelist)):
   tilist.append(titlestatus(titlelist[i]))

 
 allstatuslist=cpus+mems+powers+disks+fans+bats+vots+tilist
 intallstatuslist=[int(i) for i in allstatuslist]
 
###exit結果判斷
 exitcodestatus=titlestatus(tilist)
 exitcodestatus=int(exitcodestatus)
 print(exitcodestatus)
###layer處理
 layerlist=[cpus,mems,powers,disks,fans,bats,vots]
 halflayer=list()
 for i in range(0, 7):
  for  j in range(len(layerlist[i])):
   halflayer.append(str(i+1)+','+str(j+1))
 

 titlelayerlist=["0","1","2","3","4","5","6","7","8"]
 alllayerlist=halflayer+titlelayerlist

###value資料收集
 cpuv = CMNC(valuelist[0]).strip().split("\n")
 memv = CMNC(valuelist[1]).strip().split("\n")
 powerv = CMNC(valuelist[2]).strip().split("\n")
 diskv = CMNC(valuelist[3]).strip().split("\n")
 fanv = CMNC(valuelist[4]).strip().split("\n")
 batv = CMNC(valuelist[5]).strip().split("\n")
 votv = CMNC(valuelist[6]).strip().split("\n")
 sysv = CMNC(valuelist[7]).strip().split("\n")

###value處理
 tivaluelist=[0]
 tempvaluelist=[]
 valuelisthand=[cpuv,memv,powerv,diskv,fanv,batv,votv]
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
 allvaluelist=cpuv+memv+powerv+diskv+fanv+batv+votv+tivaluelist
 allvaluelist.append(0)
# print(allvaluelist)
### 宣告其餘需要list  ###
 objid=list()
 devicename=list()
 apiname=list()
 inserdate=list()
 tempvalue=list()
 for i in range(len(allkeylist)):
  objid.append(objectid)
  devicename.append(displayname)
  apiname.append(APIname)
  inserdate.append(function_getDataTime())
#  tempvalue.append(0)


 dictionary={'icin_host_object_id':{},'Device':{},'APIname':{},'dataKey':{},'dataValue':{},'status':{},'layer':{},'insert_date':{}}
 dataframe=pd.DataFrame(dictionary)
 dataframe['icin_host_object_id']=objid
 dataframe['Device']=devicename
 dataframe['APIname']=apiname
 dataframe['dataKey']=allkeylist
 dataframe['dataValue']=allvaluelist
 dataframe['status']=intallstatuslist
 dataframe['layer']=alllayerlist
 dataframe['insert_date']=inserdate

# dataframe.loc[dataframe.status==0,'dataValue']="""ok"""
# dataframe.loc[dataframe.status==1,'dataValue']="""warning"""
# dataframe.loc[dataframe.status==2,'dataValue']="""critical"""
 dataframe.loc[dataframe.layer=='0','dataValue']="""狀態"""
 dataframe.loc[dataframe.layer=='8','dataValue']=sysv
 print("Dataframe=\n",dataframe)
 DataFrameToSql(dataframe)
 print("Data transferred from dataframe to mysql successfully")
 
 sys.exit(exitcodestatus)
 #end







if __name__ == '__main__':
  main()
