#!/usr/bin/python3
#coding:utf-8

import psycopg2
import pandas as pd
import pymongo
import psycopg2.extras as extras
import json
import numpy as np
import time

def con_postgresql(dbn,sql):
 db = psycopg2.connect(host='192.168.39.225',
                     user='mirle',
                     password='Ml22099478!',
                     database=dbn)

 cursor = db.cursor()
 cursor.execute(sql)
 result = cursor.fetchall()
 df = pd.DataFrame(list(result))
 db.close()
 return df


def con_mongo(col):
 myclient = pymongo.MongoClient("mongodb://mirle:Ml22099478!@192.168.39.232:27017,192.168.39.233:27017,192.168.39.234:27017/?authMechanism=DEFAULT")
 mydb = myclient["STK_SDP_817_PLC"]
 mycol = mydb[col]
 mydoc = mycol.find_one(sort=[('_id', -1)])
 my_list = [mydoc]
    
 return my_list

def dif_abnor(df1,df2):
    #std
    c = df1['field'].to_list()
    #mongo
    d = df2['field'].to_list()
    e = []
    f = []
    cpf = []
    index_cpf = []
    for i in c:
     if i in d:
        continue
     else:
        e.append(i)

    for i in d:
     if i in c:
        continue
     else:
        f.append(i)

    e.sort()
    f.sort()
    ###
    for i in range(len(f)):
     cpf.append(f[i].replace(' ','_'))

    for s in cpf:
      if s in c:
       index_cpf.append(cpf.index(s))
      else:
       continue
    for idx in sorted(index_cpf, reverse = True):
     del f[idx]
    e = json.dumps(e)
    f = json.dumps(f)
    return e , f


def execute_values(conn, df, table):
  
    tuples = [tuple(x) for x in df.to_numpy()]
  
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()

dbn = 'mirlestk'
sql = 'select stk_id from stk_id_config where activate = 1'
result = con_postgresql(dbn,sql)

result.rename(columns={0:'stk_id'}, inplace=True)
result_list = result['stk_id'].tolist()

cdf1 =  pd.read_csv("C:/Users/youliang/Desktop/work/none/C1_Tag.txt",header=None)
cdf2 =  pd.read_table("C:/Users/youliang/Desktop/work/none/C2_Tag.txt",header=None)
cdf3 =  pd.read_table("C:/Users/youliang/Desktop/work/none/Power_Tag.txt",header=None)
cdf4 =  pd.read_table("C:/Users/youliang/Desktop/work/none/add.txt",header=None)
cdf = pd.concat([cdf1,cdf2,cdf3,cdf4],axis=0, ignore_index=True)
cdf.columns = ['field']
cdf_list = cdf['field'].tolist()
cdf_list.sort()
cdf_json = json.dumps(cdf_list)


database = "mirlestk"
dbUser = "mirle"
dbPwd = "Ml22099478!"
conn = psycopg2.connect(database=database, user=dbUser, password=dbPwd, host='192.168.39.225', port='5432') 



for col in result_list:
 mongo_list = con_mongo (col)
 if mongo_list == [None]:
    inserttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    nowtime = {'time':inserttime}
    df1 = pd.DataFrame([nowtime])
    stk_id_dict = {'stk_id':col}
    df2 = pd.DataFrame([stk_id_dict])
    type_dict = {'type':"column"}
    df3 = pd.DataFrame([type_dict])
    std = {'std':cdf_json}
    df4 = pd.DataFrame([std])
    abno = {'abnormal':"Nodata"}
    df5 =  pd.DataFrame([abno])
    findf = df1.join(df2).join(df3).join(df4).join(df5)
    execute_values(conn, findf, 'plc_abnormal_log')
 else:
    mongo_df = pd.DataFrame(mongo_list).T   
    nowtime = mongo_df.loc['time']
    mongo_lists = list(mongo_df.index)
    new_modgo_df = pd.DataFrame(mongo_lists)
    new_modgo_df.rename(columns={0:'field'}, inplace=True)
    e , f = dif_abnor(cdf,new_modgo_df)
    df1 = nowtime.to_frame()
    stk_id_dict = {'stk_id':col}
    df2 = pd.DataFrame([stk_id_dict])
    type_dict = {'type':"column"}
    df3 = pd.DataFrame([type_dict])
    std = {'std':e}
    df4 = pd.DataFrame([std])
    abno = {'abnormal':f}
    df5 =  pd.DataFrame([abno])
    findf = df1.join(df2).join(df3).join(df4).join(df5)
    execute_values(conn, findf, 'plc_abnormal_log')
    #pd.set_option("display.max_columns",1000000000)
    #print (findf)






