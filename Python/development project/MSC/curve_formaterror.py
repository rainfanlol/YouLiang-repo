#!/usr/bin/python3
#coding:utf-8

#import psycopg2

def main():

 #import time # 引入time
 #timeString = "2022-09-01 00:00:00" # 時間格式為字串
 #struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
 #time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
 #print(time_stamp)
 #conn=psycopg2.connect(database="mirle_msc",user="mirle",password="Ml22099478!",host="192.168.39.225",port="5432")
 #cur=conn,cursor()
 #cur.execute("insert into msc_curve_version_control(parentid,msc_ip,file_name,file_status,start_time,last_timetick,insert_date_time)",(66666666-6666))
 #from FinMind.data import DataLoader
 import psycopg2
 import pandas as pd
 import re
 import time
 from sqlalchemy import create_engine
 import os
# 取得 dataframe 資料

# 測試連線 PostgreSQL
 logfile = "/home/mirle/workspace/msc/curve_temp.log"
 if not os.path.getsize(logfile):
   print("pass")
   pass
 else:
   database = "mirle_msc"
   dbUser = "mirle"
   dbPwd = "Ml22099478!"
   characters = "'(),"
   conn = psycopg2.connect(database=database, user=dbUser, password=dbPwd, host="192.168.39.225", port="5432")
   cur=conn.cursor() 
   file = open(logfile, "r")
   for line in file.readlines():
    line = line.strip() 
    ip = line.split('/')[2]
    file_name = line.split('/')[-1].split( )[0]
    status="format_error"
    inserttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cur.execute('select uuid_generate_v4() as uuid1')
    results=cur.fetchall()
    uuid = str(tuple(results))
    uuid = re.sub("""\(|\)|\,|\'""","",uuid)
    cur.execute("insert into msc_curve_version_control(parentid,msc_ip,file_name,file_status,start_time,last_timetick,insert_date_time)VALUES(%s,%s,%s,%s,%s,%s,%s);",(uuid,ip,file_name,status,inserttime,inserttime,inserttime))
    conn.commit()

   cur.close()
   conn.close()
   with open(logfile,"r+") as f:
    read_data = f.read()
    f.seek(0)
    f.truncate() 
    print("ok")
main()
