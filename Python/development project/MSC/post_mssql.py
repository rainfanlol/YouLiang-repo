#!/usr/bin/python3
#coding:utf-8


import psycopg2
import pandas as pd
import pymssql
import psycopg2.extras as extras
from sqlalchemy import create_engine

def con_sql(dbn,sql):
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

def con_mssql(host,dbn,sql):
 db = pymssql.connect(host=host,
                     user='sa',
                     password='p@ssw0rd',
                     database=dbn)

 cursor = db.cursor()
 cursor.execute(sql)
 result = cursor.fetchall()
 df = pd.DataFrame(list(result))
 db.close()
 return df

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
result = con_sql(dbn,sql)

result.rename(columns={0:'stk_id'}, inplace=True)
result_list = result['stk_id'].tolist()
#print(result_list)
#exit()
for host in result_list:


 dbn = 'HL_SDP4STK0400'
 sql = 'select top 1 HISDT, COMMANDID, TASKNO, COMPLETECODE, ACTIVEDT, FINISHDT from HL_SDP4STK0400.dbo.HISTASK order by HISDT desc'
 result = con_mssql(host,dbn,sql)
 result.rename(columns={0:'hisdt',1:'commandid',2:'taskno',3:'completecode',4:'activedt',5:'finishdt'}, inplace=True)
 #df_reset=result.set_index('taskno')
 #print (df_reset)

 database = "mirlestk"
 dbUser = "mirle"
 dbPwd = "Ml22099478!"
 conn = psycopg2.connect(database=database, user=dbUser, password=dbPwd, host='192.168.39.225', port='5432') 
 execute_values(conn, result, 'lcs_histask_lastest_data')
"""
 engine = create_engine('postgresql://'+ dbUser +':'+ dbPwd +'@192.168.39.225:5432/' + database)
 print("opened database successfully")
 df_reset.to_sql('lcs_histask_lastest_data', engine, if_exists='append')
 print("insert data successfully")

 engine.dispose()
"""