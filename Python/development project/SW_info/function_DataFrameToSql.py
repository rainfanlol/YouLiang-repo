#!/usr/bin/python3
###把DF寫入DB

### 內部函數 ###
import sys, os, time, re, platform

### 第三方套件函數  ###
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import mysql.connector
from mysql.connector import Error
from builtins import str

def DataFrameToSqll(dataframe,delsql,uptimesql,tablename):
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
#例  conn=mysql.connector.connect(host="servicedj-mariadb",user="mspadmin",password="MIRLEau4a832019",database="icinga2",charset="utf8")
  conn=mysql.connector.connect(host=dbdict['host'],user=dbdict['user'],password=dbdict['password'],database=dbdict['database'],charset=dbdict['default-character-set'])
  cur=conn.cursor()
#  bugnum="'"+HostIP+"'"
#  delsql=f"delete from {tablename} WHERE icin_host_object_id = {objectid} and Device = {displayname} and APIname = '{apiname}'"
  cur.execute(delsql)
#  cur.execute("delete from \""+tablename+"\" WHERE icin_host_object_id = "+objectid+" and Device = \""+displayname+"\" and APIname = \""+apiname+"\"")
  conn.commit()

  engine = create_engine('mysql+pymysql://'+dbdict['user']+':'+dbdict['password']+'@'+dbdict['host']+':'+dbdict['port']+'/'+dbdict['database'])


  dataframe.to_sql(
      name=tablename,
      con=engine,
      index=False,
      if_exists='append'
  )
#  temptime=function_getDataTime()
 # uptimesql=f"UPDATE {tablename} SET insert_date = \"{temptime}\""
#  cur.execute("UPDATE \""+tablename+"\" SET insert_date = \""+temptime+"\"")
  cur.execute(uptimesql)
#  cur.execute("UPDATE \""+tablename+"\" SET insert_date = \""+temptime+"\"")
  conn.commit()
  cur.close()
 except Error as e:
   print("Error in Mysql connection=",e)
 finally:
   conn.close()
