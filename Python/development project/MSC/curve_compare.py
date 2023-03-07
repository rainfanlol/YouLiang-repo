#!/usr/bin/python3
#coding:utf-8


def main():

 #import psycopg2
 from pandas import DataFrame
 import pandas as pd
 import re
 import time
 #from sqlalchemy import create_engine
 import os
 import sys
 csv_folder = '/home/mirle/workspace/msc'
 traget = "curve"
 conf_path = '/home/mirle/workspace/msc'
###this time
 command1=f"find /nas/192_168_88_*/ -name '*.curve' -newermt '2022-09-01 08:00:00' > /home/mirle/workspace/msc/curve_thistime.txt"
 os.system(command1)

 #command2="cat /root/msc/datalist.log|awk -F '/' '{print $3,$6}'|sed 's/ /,/g'|sed 's/$/.csv/g' > /root/msc/curve_thistime.txt"
 #os.system(command2)

 command3=f"sed -i '1i\list' /home/mirle/workspace/msc/curve_thistime.txt"
 os.system(command3)

 nasdf = pd.read_csv('/home/mirle/workspace/msc/curve_thistime.txt')
 #print(nasdf)

###last time

 #command4=f"sed -i '1i\list' /root/msc/curve_lasttime.txt"
 #os.system(command4)

 lastdf = pd.read_csv('/home/mirle/workspace/msc/curve_lasttime.txt')
 

###比較
 only_result = nasdf.merge(lastdf, how='outer', indicator=True).loc[lambda x : x['_merge'] == 'left_only'].drop(columns=['_merge'])
 print(only_result)
 #only_result.to_csv('/home/mirle/workspace/msc/1206.csv')
###轉list
 list_of_single = only_result['list'].tolist()
 if len(list_of_single):
  for i in list_of_single:
    string_list = i.split("/")
    ips = string_list[2]
    filename = string_list[5]
    command5='mkdir -p '+csv_folder+'/'+traget+'/nas/'+ips
    os.popen(command5)
    command6=f"/home/mirle/workspace/msc/log2csv_centos7/log2csv_centos7 {conf_path}/curve_log_conf.csv "
    command7=f"{i} {csv_folder}/{traget}/nas/{ips}/{filename}.csv "
    command8=f" >> {csv_folder}/curve_temp.log "
    concat=command6+' '+command7+' '+command8
    #print(concat)
    os.system(concat)

 else:
  print("do not")
  sys.exit()

###去掉不能轉檔的空目錄
 command9='find ' +csv_folder+'/'+traget+ ' -type d -empty -delete'
 os.popen(command9)

###lasttime複寫
 command10='cp /home/mirle/workspace/msc/curve_thistime.txt /home/mirle/workspace/msc/curve_lasttime.txt'
 os.popen(command10)
 
main()
