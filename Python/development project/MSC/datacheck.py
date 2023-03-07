#!/usr/bin/python3
#coding:utf-8

import pymysql
import pandas as pd
import json
import re
def con_sql(db,sql):
 db = pymysql.connect(host='172.16.111.135',
                     user='root',
                     password='p@ssw0rd',
                     database=db,
                     charset='utf8')

 cursor = db.cursor()
 cursor.execute(sql)
 result = cursor.fetchall()
 df = pd.DataFrame(list(result))
 db.close()
 return df

db = 'gce'
sql = 'select * from gce.iot_sensor_data_copy_20221110 order by id limit 0,100'
result = con_sql(db,sql)
#result.columns = list('abcde')
#result.columns = ['id','SensorName','sid','SensorData','CreateDate']
#sensor_name_list = result[3].unique()
#print (sensor_name_list)

##各sensor name筆數
#print(result[1].value_counts(sort=True))

##json比對
json_obj = result[3].values.tolist()
for i in range(100):
 json_data = []
 json_data = json_obj[i]
 stocks = json.loads(json_data)
 stocks_list = []
 for k,v in stocks.items():
   stocks_list.append(k)
 result.at[i,3] = stocks_list
#print(result)

result[[3]] = result[[3]].astype(str)
#result.rename(columns={1:'sensor_name',2:'sid',3:'sensor_data'})
#print(result)
sensor_group = result.groupby([1])


#split_data = result[3].str.split(',', expand=True)
#split_data.to_csv('C:/Users/youliang/Desktop/work/金像/split_data.csv')


sensor_data = sensor_group[3].value_counts()
sensor_data.to_csv('C:/Users/youliang/Desktop/work/金像/sensor_data.csv')
sid = sensor_group[2].value_counts()
#sid.info()
#sid.columns = ['SensorName','sid']
sid.to_csv('C:/Users/youliang/Desktop/work/金像/sid.csv')

#print(stocks_list)
#with open("C:/Users/youliang/Desktop/work/金像/output.txt", "w") as opfile:
    #for i in range(len(stocks_list)):
        #s = (re.sub(r"['{ },]*", '', str(stocks_list[i]))+',').replace(':', ',')
        #opfile.write(s)    
