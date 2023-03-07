#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#功能:監控某支援SNMP功能儀器的程序,依照各使用者及其程序使用量去做排序(依順序:使用者名稱>CPU使用率>MEM使用率)

### 內部函數 ###
import sys, os, time, re, platform

### 第三方套件函數  ###
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import mysql.connector
from mysql.connector import Error
from function_you.function_checkstatus import *

### 命令行輸入參數 ###
command = sys.argv
version = command[1]
community = command[2]
hostip = command[3]
port = command[4]
low_level = command[5]
high_level = command[6]


### 自定義變數  ###

APIname="ProcessByUser"
par = [version,community,hostip,port]
oidtitle = '.1.3.6.1.4.1.2021.54'
processoid = ".3.1.2"

### 自定義函式  ###
def function_getDataTime():
        localDateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return localDateTime


#def function_getDataTimes():
#        localDateTime = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
#        return localDateTime

#def function_getday():
#        localDateTime = time.strftime("%m-%d", time.localtime())
#        return localDateTime


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
#	revalue = function_ospopen("sudo mysql --login-path=remote -D %s -e \"%s\"" % (database,command))
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
  result = os.popen("snmpwalk -m UCD-SNMP-MIB -v "+par[0]+" -c "+par[1]+" "+par[2]+":"+par[3]+" "+oidtitle+""+n1)
  return result

def CMN(n2):
  result = os.popen("snmpwalk -Oqv -m UCD-SNMP-MIB -r 5 -t 7 -v "+par[0]+" -c "+par[1]+" "+par[2]+":"+par[3]+" "+oidtitle+""+n2+""" | sed 's/"//g'""").read()
  return result

def paa():
  print ('############################################################################################################')

  ### df to db  ###
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
  cur.execute("delete from mirle_mon_Service_LinuxPS WHERE icin_host_object_id = "+objectid+" and Device = \""+displayname+"\" and APIname = \"ProcessByUser\"")
  conn.commit()
  ### insertion data from dataframe ###
  for(row,rs) in dataframe.iterrows():
    icin_host_object_id=str(int(rs[0]))
    Device=str(rs[1])
    APIname=rs[2]
    dataKey=rs[3]
    dataValue=str(rs[4])
    status=str(rs[5])
    layer=str(rs[6])
    insert_date=rs[7]
    ### sql query ###
    query="insert into mirle_mon_Service_LinuxPS(icin_host_object_id,Device,APIname,dataKey,dataValue,status,layer,insert_date) values("+ icin_host_object_id +",'"+ Device +"','"+ APIname +"','"+ dataKey +"','"+ dataValue +"','"+ status +"','"+ layer +"','"+ insert_date +"')"
    ### print(query) ###
    cur.execute(query)
  conn.commit()
  cur.execute("UPDATE mirle_mon_Service_LinuxPS SET insert_date = \""+function_getDataTime()+"\";")
  conn.commit()
  cur.close()
 except Error as e:
   print("Error in Mysql connection=",e)
 finally:
   conn.close()
### 用bash把資料寫入sql  ###
#def DataFrameToSql(dataframe):


### 寫入InfluxDB函數  ###
def DataToInfluxDB(duser,secvalue):
 #print("Monitoring data overview:")
 for w in range(len(duser)):
   #print("User Name:"+duser[w]+"\tCPU usage="+secvalue[w][0]+"%\tMemory usage="+secvalue[w][1]+"% |"+duser[w]+" CPU%="+secvalue[w][0]+" "+duser[w]+" Mem%="+secvalue[w][1])
   #print(duser[w]+":"+secvalue[w][0]+":"+secvalue[w][1]+"|"+duser[w]+" CPU%="+secvalue[w][0]+" "+duser[w]+" Mem%="+secvalue[w][1])
   print("| "+duser[w]+" CPU%="+secvalue[w][0]+" "+duser[w]+" Mem%="+secvalue[w][1],end=';')
 return

### 判斷status  ###
def function_status():
 statusvalue=list()
 
 
 return statusvalue


### 定義OBJ和NAME變數  ###
#displayname = "123"
#objectid = "456"

displayname = function_icinga_displayname(hostip)
objectid = function_icinga_objectid(hostip,displayname)

### 主程式  ###
def main() :


### 函數回傳原始資料格式  ###
 result = CMN(processoid)

### 正規化不規則空格和把字串分為二維串列  ###
 ptn = re.compile("\s+")
 lines = result.strip().split("\n")


### 宣告空list  ###
 cuser=list()
 CPU=list()
 Mem=list()
 Pid=list()
 CMD1=list()


 
### 切欄  ###
 for line in lines:
    items = ptn.split(line,4) #切不規則空格

    ### 建立各欄 list  ###
    cuser.append(items[0])
    CPU.append(items[1])
    Mem.append(items[2])
    Pid.append(items[3])
    CMD1.append(items[4])


###Command長度處理
 CMD=CMD1[1:]
 for i in range(len(CMD)):
    if len(CMD[i])>70:
      CommandPathPar=CMD[i].split(" ",1)

      if '/' not in CommandPathPar[0]:
        tempResult=CommandPathPar[0]
        tempResult=tempResult[:69]
        CMD[i]=tempResult
      else:
       CommandFirPath=CommandPathPar[0].split('/')[1]
       CommandFinPath=CommandPathPar[0].split('/')[-1]
       CommandResult=CommandFinPath+' '+CommandPathPar[1]
       CMD[i]=CommandResult


       if(len(CommandResult)>70):
         CommandResult=CommandResult[:69]
         CMD[i]=CommandResult
       else:
         PathFstring=f"/{CommandFirPath}/.../{CommandFinPath}"  
         DotPathPar=PathFstring+' '+CommandPathPar[1]
         DotPathParsult=DotPathPar[:69]
         CMD[i]=DotPathParsult
    else: 
     continue
### 找出各user和標頭user去掉  ###
 duser = list(set(cuser))
# print(duser)
 duser.remove('USER')
 duser.sort()
###反轉元素
 duser.reverse()


### dataframe行列全顯示  ###
 pd.set_option('display.max_columns', None)
 pd.set_option('display.max_rows', None)


### 把user寫入字典轉DataFrame格式  ###
 cuser.remove('USER')
 title1={"USER":cuser}
 title={"USER":duser}
 traUser=pd.DataFrame(title1)
 tradUser=pd.DataFrame(title)
 

### 把CPU和MEM資料刪除原本title ###
 CPU.remove('%CPU')
 Mem.remove('%MEM')

### 把list內資料轉float  ###
 floatCPU=[float(i) for i in CPU]
 floatMem=[float(i) for i in Mem]

### list轉字典格式  ###
 listcpu={"%CPU":CPU}
 listmem={"%MEM":Mem}
 title2={"%CPU":floatCPU}
 title3={"%MEM":floatMem}


### 字典轉DataFrame格式  ###
 traCPU,traMem=pd.DataFrame(title2),pd.DataFrame(title3)
 traCPU=traCPU.round(1)
 traMem=traMem.round(1)
 listtracpu,listtramem=pd.DataFrame(listcpu),pd.DataFrame(listmem)


### 處理pid&cmd並寫入Dataframe  ###
 Pid.remove('PID')
# CMD.remove('CMD')
 title4 ,title5= {"PID":Pid},{"CMD":CMD}
 traPID, traCMD=pd.DataFrame(title4), pd.DataFrame(title5)


### 合併Dataframe並依使用者排序 ###
 res = pd.concat([traUser,traCPU,traMem,traPID, traCMD],axis=1)
# print(res)
### 各程序依CPU使用量排序  ###
 res = res.sort_values(["USER","%CPU","%MEM"],ascending=False)
 resnu = res.drop(["USER"], axis=1)
 tostatusvalue = res.drop(["USER","PID","CMD"], axis=1)

### 宣告使用量變數為list  ###
 layer=list()
 clayer=list()

### 各使用者使用cpu&mem總和  ###
 usetotal=res.groupby('USER').sum().round(1)
 usetotal.sort_values('USER', ascending = False, inplace=True)
 tovaluelist=usetotal
 sectotalvaluedf=tovaluelist.astype(str)

### 各使用者賦予layer  ###
 for i in range(len(duser)):
   layer.append(i+1);
   userrow=res[res['USER'] == duser[i]]


###計算各程序數量並存入layer的list###
   for j in range (len(userrow)):
    layernum=str(i+1)+','+str(j+1)
    clayer.append(layernum);

### layer寫入dataframe  ###
 res['layer']=clayer
 usetotal['layer']=layer

### 各欄list處理 ###
 ### datevalue&api&obj&device ###
 # 先宣告空list #
 totalobj=list()
 totaldev=list()
 totalapi=list()
 totaldate=list()
 totalstatus=list()

 # 程序和使用者與篩選後結果合併 #
 cuser.sort()
 cuser.reverse()
 totalkey=cuser+duser
# print(totalkey)
 totallayer=clayer+layer
# print(totallayer)
 for i in range(len(totalkey)):
  totalobj.append(objectid)
  totaldev.append(displayname)
  totalapi.append(APIname)
  totaldate.append(function_getDataTime())
  totalstatus.append(0)


### 處理status  ###
 statusdf=pd.concat([tostatusvalue,sectotalvaluedf],axis=0)
 statusdf['status']=totalstatus
 statusdf=statusdf.rename(columns = {'%CPU':'CPU','%MEM':'MEM'})
 statusdf['CPU']=statusdf['CPU'].astype(float)
 statusdf['MEM']=statusdf['MEM'].astype(float)
  # 1&2為測試水位 #
 statusdf.loc[statusdf.CPU>float(low_level),'status'] = 1
 statusdf.loc[statusdf.MEM>float(low_level),'status'] = 1
 statusdf.loc[statusdf.CPU>float(high_level),'status'] = 2
 statusdf.loc[statusdf.MEM>float(high_level),'status'] = 2
 totalstatus=statusdf.drop(["CPU","MEM"], axis=1)
 totalstatus=totalstatus['status'].values.tolist()
# print(totalstatus)

###exit code 判斷
 ExitCodeStatus=TitleStatus(totalstatus)
 ExitCodeStatus=int(ExitCodeStatus)


 # datavalue處理 #
 resnu = resnu.astype(str)

 # for datavalue欄位把dataframe轉list格式#
 firvalue = resnu.values.tolist()
 secvalue=sectotalvaluedf.values.tolist()

 # 把各項程序CPU&MEM使用量加上pid&cmd和CPU&MEM總量的list合併  #
 totalvalue=firvalue+secvalue
# print(totalvalue)
 ### 多維list轉一維處理和字串格式化  ###
 firserlist=list()
 secserlist=list()
 for i in range(len(firvalue)):
   echo=f'"{firvalue[i][0]}","{firvalue[i][1]}","{firvalue[i][2]}","{firvalue[i][3]}"'
   firserlist.append(echo)

 for j in range(len(secvalue)):
   echo=f'"{secvalue[j][0]}","{secvalue[j][1]}"'
   secserlist.append(echo)

 totalvalue=firserlist+secserlist


### 寄告警信 
 #if ( mailservice == 1):
 mailmes=list()
 for i in range(len(duser)):
   if  float(secvalue[i][0]) > float(low_level)  or  float(secvalue[i][1]) > float(low_level) :
     mailmes.append(f'UserName:{duser[i]} : CPU usage={secvalue[i][0]}% : Memory usage={secvalue[i][1]}%')
 if len(mailmes) != 0:
  Strmailmes=";".join(mailmes)
  print(Strmailmes)
 else:
  #print(" ")
  print("No abnormality or abnormal state recovery")



 #print(" ")
# print("-------------------------------------------")

### 處理layer=0  ###

 totalobj.append(objectid)
 totaldev.append(displayname)
 totalapi.append(APIname)
 totalstatus.append(0)
# totalstatus.append(0)
 totallayer.append(0)
 totalkey.append("User Name")
 layer0=f'"CPU%","MEM%","PID","CMD"'
 totalvalue.append(layer0)
 totaldate.append(function_getDataTime())

###測試matavalue長度
# for i in range(len(totalvalue)):
#   print (i,len(totalvalue[i]))
# print(totalvalue[173])
# print(len(totalvalue[173]))
### 把各項處理好LIST資料轉df呼叫函數送進db內  ###
 
 dictionary={'icin_host_object_id':{},'Device':{},'APIname':{},'dataKey':{},'dataValue':{},'status':{},'layer':{},'insert_date':{}}
 dataframe=pd.DataFrame(dictionary)
 dataframe['icin_host_object_id']=totalobj
 dataframe['Device']=totaldev
 dataframe['APIname']=totalapi
 dataframe['dataKey']=totalkey
 dataframe['dataValue']=totalvalue
 dataframe['status']=totalstatus
 dataframe['layer']=totallayer
 dataframe['insert_date']=totaldate


### 驗證最後結果並存入DB  ###
 #print("Dataframe=\n",dataframe)

 DataFrameToSql(dataframe)
 #print("Data transferred from dataframe to mysql successfully")


 DataToInfluxDB(duser,secvalue)
 #print("Data transferred from dataframe to influxdb successfully")




 sys.exit(ExitCodeStatus)
 #end


if __name__ == '__main__':
  main()



