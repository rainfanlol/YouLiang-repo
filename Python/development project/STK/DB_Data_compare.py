#!/usr/bin/python3
#coding:utf-8

import psycopg2
import pandas as pd
import pymongo
import psycopg2.extras as extras
import json
import numpy as np
import time
import base64
from configparser import ConfigParser

def con_postgresql(post_host,post_user,post_decry_passw,post_dbn,sql):
 db = psycopg2.connect(host=post_host,
                     user=post_user,
                     password=post_decry_passw,
                     database=post_dbn)

 cursor = db.cursor()
 cursor.execute(sql)
 result = cursor.fetchall()
 df = pd.DataFrame(list(result))
 db.close()
 return df


def con_mongo(mongo_conn,mongo_dbn,col):
 myclient = pymongo.MongoClient(mongo_conn)
 mydb = myclient[mongo_dbn]
 mycol = mydb[col]
 mydoc = mycol.find_one(sort=[('_id', -1)])
 my_list = [mydoc]
    
 return my_list

def dif_abnor(df1,df2):
    #std
    c = df1['field'].to_list()
    c_temp = []
    ###大寫
    c1 = []
    for x in c:
        c1.append(x.upper())

    #mongo
    d = df2['field'].to_list()
    d1 = []
    for z in d:
        d1.append(z.replace(' ','_').upper())
    
    #e = []
    f = []
    cpf = []
    std_only = []
    
    index_cpf = []
    index_std_only = []
    for ii in c1:
     if ii in d1:
        continue
     else:
        std_only.append(ii)


    for q in std_only:
        if q in  c1:
          index_std_only.append(c1.index(q))
        else:
         continue
    for u in index_std_only:
        c_temp.append(c[u])
    for i in d:
     if i in c:
        continue
     else:
        f.append(i)
    c1.sort()
    #e.sort()
    f.sort()
    ###
    for i in range(len(f)):
     cpf.append(f[i].replace(' ','_').upper())
    for s in cpf:
      if s in c1:
       index_cpf.append(cpf.index(s))
      else:
       continue
    for idx in sorted(index_cpf, reverse = True):
     del f[idx]

    ###改後相同值
    same_list = []

    for i in c:
        if i in d:
            same_list.append(i)

    cp_c = c
    cp_d = d
    add_only_same_std = same_list+c_temp
    add_only_same_abo = same_list+f

    for m in cp_c[:]:
    
       if m in add_only_same_std:
        cp_c.remove(m)
    for n in cp_d[:]:
       if n in add_only_same_abo:
        cp_d.remove(n)

    
    cp_c.sort()
    cp_d.sort()


    dif_std =pd.DataFrame(cp_c)
    dif_abo =pd.DataFrame(cp_d)
    dif_std.rename(columns={0:'std'}, inplace=True)
    dif_abo.rename(columns={0:'abnormal'}, inplace=True)
    H_dif_col = pd.concat([dif_std,dif_abo],axis = 1)

    ###判斷ii
    if "C1_Lifter_Miileage" in f and "C1_Lifter_Mileage" in c_temp:
        temp_ii={'std':["C1_Lifter_Mileage"],'abnormal':["C1_Lifter_Miileage"]}
        c1_df_ii=pd.DataFrame.from_dict(temp_ii)
        c_temp.remove("C1_Lifter_Mileage")
        f.remove("C1_Lifter_Miileage")
        H_dif_col = pd.concat([H_dif_col,c1_df_ii])
        

    if "C2_Lifter_Miileage" in f and "C2_Lifter_Mileage" in c_temp:
        temp_ii={'std':["C2_Lifter_Mileage"],'abnormal':["C2_Lifter_Miileage"]}
        c2_df_ii=pd.DataFrame(temp_ii)
        c_temp.remove("C2_Lifter_Mileage")
        f.remove("C2_Lifter_Miileage")
        H_dif_col = pd.concat([H_dif_col,c2_df_ii])
        

    H_dif_col.reset_index(drop=True, inplace=True)
    df_e = pd.DataFrame(c_temp)
    df_f = pd.DataFrame(f)
    df_e.rename(columns={0:'std'}, inplace=True)
    df_f.rename(columns={0:'abnormal'}, inplace=True)

    ### df_e:std表  df_f:abnormal表
    return df_e , df_f , H_dif_col


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

def decryption(password):
    try:
        input_value = base64.b64decode(password).decode("utf-8")
        key = 'Z&sg6nu7A79tP#g#a6Q@&1UejtVo^&ys*SH^sOtTW*!WiUGmS19L#j%2daBBFs!IlvS*!9u3Ht@qKVum'
        dec_str = ""
        for i,j in zip(input_value.split("_")[:-1], key): # i 為加密字符，j為秘鑰字符
            temp = chr(int(i) - ord(j)) 
            dec_str = dec_str+temp
    except Exception as e:
        print("error! decryption")
        raise e
    return dec_str

def auto_df_to_db(df1,df2,data_type,column_name,std,abnormal):
    try:
        type_dict = {'type':data_type}
        df_type = pd.DataFrame([type_dict])
        set_column = {"column_name":column_name}
        df_column = pd.DataFrame([set_column])
        set_std = {"std":std}
        df_std = pd.DataFrame([set_std])
        set_abonormal = {"abnormal":abnormal}
        df_abonormal = pd.DataFrame([set_abonormal])
        result_df = pd.concat([df1,df2,df_type,df_column,df_std,df_abonormal],axis = 1)
        execute_values(conn, result_df, 'plc_abnormal_log')
    except:
        print("auto insert data error!")

#get_db_info
configur = ConfigParser()
configur.read('config.ini')
post_dbn = configur.get('postgresql', 'database')
post_host = configur.get('postgresql', 'ip')
post_user = configur.get('postgresql', 'user')
post_passw = configur.get('postgresql', 'password')
post_decry_passw = decryption(post_passw)
post_port = configur.get('postgresql', 'port')
sql = 'select stk_id from stk_id_config where activate = 1'
result = con_postgresql(post_host,post_user,post_decry_passw,post_dbn,sql)

mongo_dbn = configur.get('mongo_db', 'database')
mongo_host = configur.get('mongo_db', 'ip_port')
mongo_user = configur.get('mongo_db', 'user')
mongo_passw = configur.get('mongo_db', 'password')
mongo_decry_passw = decryption(post_passw)
mongo_conn = f"mongodb://{mongo_user}:{mongo_decry_passw}@{mongo_host}/?authMechanism=DEFAULT"



result.rename(columns={0:'stk_id'}, inplace=True)
result_list = result['stk_id'].tolist()

cdf1 =  pd.read_csv("C1_Tag.txt",header=None)
cdf2 =  pd.read_table("C2_Tag.txt",header=None)
cdf3 =  pd.read_table("Power_Tag.txt",header=None)
cdf4 =  pd.read_table("add.txt",header=None)
cdf = pd.concat([cdf1,cdf2,cdf3,cdf4],axis=0, ignore_index=True)
cdf.columns = ['field']
cdf_list = cdf['field'].tolist()
cdf_list.sort()
cdf_json = json.dumps(cdf_list)

conn = psycopg2.connect(database=post_dbn, user=post_user, password=post_decry_passw, host=post_host, port=post_port) 

setrawdata = pd.read_csv("std.csv")

#setrawdata = pd.read_excel(io="std.xlsx")
#判斷相同數值設定
#set_same_list = setrawdata['same_value'].dropna(axis=0,how='all').tolist()
#判斷不相同數值設定
#set_dif_list = setrawdata['different_value'].dropna(axis=0,how='all').tolist()
#最大&最小設定值
sheet = setrawdata[['name','minimum','maximum']]
sheet = sheet.copy()
sheet.dropna(axis=0,subset = ["minimum"],inplace=True)

result_list = ["TSTK0116"]
for col in result_list:

 lift_str = col[0:4]
 right_str = col[4:8]
 con_str = f"{lift_str}_{right_str}"
 #mongo_list = con_mongo(mongo_conn,mongo_dbn,con_str)
 mongo_list = con_mongo(mongo_conn,mongo_dbn,col)
 if mongo_list == [None]:
    inserttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    nowtime = {'time':inserttime}
    df1 = pd.DataFrame([nowtime])
    stk_id_dict = {'stk_id':col}
    df2 = pd.DataFrame([stk_id_dict])
    type_dict = {'type':"column"}
    df3 = pd.DataFrame([type_dict])    
    std = {'std':"null"}
    column_dict = {'column_name':"null"}
    df4 = pd.DataFrame([column_dict]) 
    df5 = pd.DataFrame([std])
    abno = {'abnormal':"no data"}
    df6 =  pd.DataFrame([abno])
    findf = df1.join(df2).join(df3).join(df4).join(df5).join(df6)
    execute_values(conn, findf, 'plc_abnormal_log')
 else:

    ###value_compare
    mongo_value = pd.DataFrame(mongo_list).T.reset_index().rename(columns = {'index':'name', 0:'value'})
    concat_value = pd.merge(sheet,mongo_value,how="inner",on=["name"])
    concat_value['value'].astype(float)
    concat_value['result'] = np.where((concat_value['minimum']<=concat_value['value'])&(concat_value['maximum']>=concat_value['value']),'pass','error')
    error_value = concat_value[concat_value['result'] == 'error']
    std_df = error_value[['name','minimum','maximum']]
    abno_df = error_value[['name','value']] 
    std_df = std_df.copy()
    std_df['std'] = std_df['minimum'].map(str)+" ~ "+std_df['maximum'].map(str)
    abno_df = abno_df.copy()
    abno_df['abnormal'] = abno_df['value'].map(str)
    df7 = std_df['std'].reset_index(drop=True)
    df8 = abno_df['abnormal'].reset_index(drop=True)
    type_dict = {'type':"data"}
    df6 = pd.DataFrame([type_dict])
    df10 = std_df['name'].reset_index(drop=True)  

       
    ###col_compare
    mongo_df = pd.DataFrame(mongo_list).T   
    nowtime = mongo_df.loc['time']
    temp_time = nowtime.iloc[0]
    mongo_lists = list(mongo_df.index)
    new_modgo_df = pd.DataFrame(mongo_lists)
    new_modgo_df.rename(columns={0:'field'}, inplace=True)
    df_e , df_f , H_dif_col = dif_abnor(cdf,new_modgo_df)
    df1 = nowtime.to_frame()
    stk_id_dict = {'stk_id':col}
    df2 = pd.DataFrame([stk_id_dict])
    type_dict = {'type':"column"}
    df3 = pd.DataFrame([type_dict])
    temp_df = pd.concat([df_e,df_f]).fillna("null").reset_index(drop=True)
    column_dict = {"column_name":"null"}
    df9 = pd.DataFrame([column_dict])
    
    ###Specific condition judgment
    #Encode Value check
    value_pass_df = concat_value[concat_value['result'] == 'pass']
    encode1_list_df = value_pass_df[[True if i in ['C1_T1_Encode_Value','C1_T2_Encode_Value',\
        'C1_T3_Encode_Value','C1_T4_Encode_Value','C1_T5_Encode_Value','C1_T6_Encode_Value',\
            'C1_T7_Encode_Value','C1_T8_Encode_Value'] \
        else False for i in value_pass_df['name']]]
    encode1_list = encode1_list_df['value'].tolist()
    if len(set(encode1_list)) == 1:
        #traveling_c1
        trave_position1_df = value_pass_df[[True if i in ['C1_Traveling_Position']\
        else False for i in value_pass_df['name']]]
        trave1_value_list = trave_position1_df['value'].tolist()
        if trave1_value_list[0] == encode1_list[0]:
            pass
        else:    
            std_Trave1 = "Traveling Position數值範圍等同於T1-T8 Encode Value"
            Trave1_abo_str = f"Traveling Position = {trave1_value_list[0]} - Encode Value = {encode1_list[0]}"
            auto_df_to_db(df1,df2,"data","C1_Traveling_Position",std_Trave1,Trave1_abo_str)
    else:
        std_encode1 = "C1 8顆走行馬達Encode Value相同"
        abo_encode1 = f"八顆行走馬達數據為 : {encode1_list}"
        auto_df_to_db(df1,df2,"data","C1_Tx_Encode_Value",std_encode1,abo_encode1)

    encode2_list_df = value_pass_df[[True if i in ['C2_T1_Encode_Value','C2_T2_Encode_Value',\
        'C2_T3_Encode_Value','C2_T4_Encode_Value','C2_T5_Encode_Value','C2_T6_Encode_Value',\
            'C2_T7_Encode_Value','C2_T8_Encode_Value'] \
        else False for i in value_pass_df['name']]]
    encode2_list = encode2_list_df['value'].tolist()
    if len(set(encode2_list)) == 1:
        #traveling_c2
        trave_position2_df = value_pass_df[[True if i in ['C2_Traveling_Position']\
        else False for i in value_pass_df['name']]]
        trave2_value_list = trave_position2_df['value'].tolist()
        if trave2_value_list[0] == encode2_list[0]:
            pass
        else:
            std_Trave2 = "Traveling Position數值範圍等同於T1-T8 Encode Value"
            Trave2_abo_str = f"Traveling Position = {trave2_value_list[0]} - Encode Value = {encode2_list[0]}"
            auto_df_to_db(df1,df2,"data","C2_Traveling_Position",std_Trave2,Trave2_abo_str)
    else:
        std_encode2 = "C2 8顆走行馬達Encode Value相同"
        abo_encode2 = f"八顆行走馬達數據為 : {encode2_list}"
        auto_df_to_db(df1,df2,"data","C2_Tx_Encode_Value",std_encode2,abo_encode2)
    
    #c1 Rotating Position check
    rota_position_df = value_pass_df[[True if i in ['C1_Rotating_Position','C1_R1_Encode_Value']\
        else False for i in value_pass_df['name']]]
    rota_list = rota_position_df['value'].tolist()
    if len(set(rota_list)) == 1:
        pass
    else:
        std_rota1 = "C1 Rotating Position與R1 Encoder Value數值相同"
        abo_rota1 = f"R1_Encode_Value = {rota_list[1]} - Rotating Position = {rota_list[0]}"
        auto_df_to_db(df1,df2,"data","C1_Rotating_Position",std_rota1,abo_rota1)

    #c2 Rotating Position check
    c2_rota_position_df = value_pass_df[[True if i in ['C2_Rotating_Position','C2_R1_Encode_Value']\
        else False for i in value_pass_df['name']]]
    c2_rota_list = c2_rota_position_df['value'].tolist()
    if len(set(c2_rota_list)) == 1:
        pass
    else:        
        std_rota2 = "C2 Rotating Position與R1 Encoder Value數值相同"
        abo_rota2 = f"R2_Encode_Value = {c2_rota_list[1]} - Rotating Position = {c2_rota_list[0]}"
        auto_df_to_db(df1,df2,"data","C2_Rotating_Position",std_rota2,abo_rota2)

    #c1 Forking Position check
    c1_fork_position_df = value_pass_df[[True if i in ['C1_F1_Encode_Value','C1_F2_Encode_Value','C1_Forking_Position']\
        else False for i in value_pass_df['name']]]
    c1_fork_list = c1_fork_position_df['value'].tolist()
    if len(set(c1_fork_list)) == 1:
        pass
    else:
        std_fork1 = "Forking_Position數值等同F1_Encode_Value、F2_Encode_Value"
        abo_fork1 = f"F1_Encode_Value = {c1_fork_list[0]} - F2_Encode_Value = {c1_fork_list[1]} - Forking_Position = {c1_fork_list[2]}"
        auto_df_to_db(df1,df2,"data","C1 Forking Position",std_fork1,abo_fork1)

    #c2 Forking Position check
    c2_fork_position_df = value_pass_df[[True if i in ['C2_F1_Encode_Value','C2_F2_Encode_Value','C2_Forking_Position']\
        else False for i in value_pass_df['name']]]
    c2_fork_list = c2_fork_position_df['value'].tolist()
    if len(set(c2_fork_list)) == 1:
        pass
    else:
        std_fork2 = "Forking_Position數值等同F1_Encode_Value、F2_Encode_Value"
        abo_fork2 = f"F1_Encode_Value = {c2_fork_list[0]} - F2_Encode_Value = {c2_fork_list[1]} - Forking_Position = {c2_fork_list[2]}"
        auto_df_to_db(df1,df2,"data","C2 Forking Position",std_fork2,abo_fork2)

    #Crane Moving and Status 
    #c1 period cycle
    c1_period_cycle_df = value_pass_df[[True if i in ['C1_Move_Period_Cycle_1','C1_Move_Period_Cycle_2']\
        else False for i in value_pass_df['name']]]
    c1_period_cycle_list = c1_period_cycle_df['value'].tolist()
    if len(set(c1_period_cycle_list)) == 1 and c1_period_cycle_list[0] == 1:
        c1_std_cycle = "Move Period Cycle 1 和 Move Period Cycle 2 不能同時 = 1"
        c1_abo_cycle = f"C1 cycle 1 = {c1_period_cycle_list[0]} - C1 cycle 2 = {c1_period_cycle_list[1]}"
        auto_df_to_db(df1,df2,"data","C1 Move Period Cycle",c1_std_cycle,c1_abo_cycle)
    else:
        pass
    #c2 period cycle
    c2_period_cycle_df = value_pass_df[[True if i in ['C2_Move_Period_Cycle_1','C2_Move_Period_Cycle_2']\
        else False for i in value_pass_df['name']]]
    c2_period_cycle_list = c2_period_cycle_df['value'].tolist()
    if len(set(c2_period_cycle_list)) == 1 and c2_period_cycle_list[0] == 1:
        c2_std_cycle = "Move Period Cycle 1 和 Move Period Cycle 2 不能同時 = 1"
        c2_abo_cycle = f"C2 cycle 1 = {c2_period_cycle_list[0]} - C2 cycle 2 = {c2_period_cycle_list[1]}"
        auto_df_to_db(df1,df2,"data","C2 Move Period Cycle",c2_std_cycle,c2_abo_cycle)
    else:
        pass

    #c1 Period Forking 
    c1_period_forking_df = value_pass_df[[True if i in ['C1_Move_Period_Forking_1','C1_Move_Period_Forking_2']\
        else False for i in value_pass_df['name']]]
    c1_period_forking_list = c1_period_forking_df['value'].tolist()
    if len(set(c1_period_forking_list)) == 1 and c1_period_forking_list[0] == 1:
        c1_std_forking = "Move Period Forking 1 和 Move Period Forking 2 不能同時 = 1"
        c1_abo_forking = f"C1 forking 1 = {c1_period_forking_list[0]} - C1 forking 2 = {c1_period_forking_list[1]}"
        auto_df_to_db(df1,df2,"data","C1 Move Period Forking",c1_std_forking,c1_abo_forking)
    else:
        pass

    #c2 Period Forking 
    c2_period_forking_df = value_pass_df[[True if i in ['C2_Move_Period_Forking_1','C2_Move_Period_Forking_2']\
        else False for i in value_pass_df['name']]]
    c2_period_forking_list = c2_period_forking_df['value'].tolist()
    if len(set(c2_period_forking_list)) == 1 and c2_period_forking_list[0] == 1:
        c2_std_forking = "Move Period Forking 1 和 Move Period Forking 2 不能同時 = 1"
        c2_abo_forking = f"C2 forking 1 = {c2_period_forking_list[0]} - C2 forking 2 = {c2_period_forking_list[1]}"
        auto_df_to_db(df1,df2,"data","C2 Move Period Forking",c2_std_forking,c2_abo_forking)
    else:
        pass
    
    
    if len(set(c1_period_cycle_list)) == 1 and len(set(c1_period_forking_list)) == 1 and c1_period_cycle_list[0] == 0:
        c1_std_zero = "Move Cycle 1&2 和 Move Forking 1&2 不能同時 = 0"
        c1_abo_value = f"C1 cycle = {c1_period_cycle_list[0]} - C1 forking = {c1_period_forking_list[0]}"
        auto_df_to_db(df1,df2,"data","C1 Move Period Cycle and Forking",c1_std_zero,c1_abo_value)
    else:
        pass

    if len(set(c2_period_cycle_list)) == 1 and len(set(c2_period_forking_list)) == 1 and c2_period_cycle_list[0] == 0:
        c2_std_zero = "Move Cycle 1&2 和 Move Forking 1&2 不能同時 = 0"
        c2_abo_value = f"C2 cycle = {c2_period_cycle_list[0]} - C2 forking = {c2_period_forking_list[0]}"
        auto_df_to_db(df1,df2,"data","C2 Move Period Cycle and Forking",c2_std_zero,c2_abo_value)
    else:
        pass

    ###some_name_dif
    col_dif_df = pd.concat([df1,df2,df3,df9,H_dif_col],axis = 1)
    col_dif_df["time"] = temp_time
    col_dif_df["stk_id"] = col
    col_dif_df["type"] = "column" 
    col_dif_df["column_name"] = "null"

    
    if 'std' in col_dif_df.columns:
        execute_values(conn, col_dif_df, 'plc_abnormal_log')
    else:
        pass
    

    ###result_value_insert
    value_compare_df = pd.concat([df1,df2,df6,df10,df7,df8],axis = 1)
    value_compare_df.rename(columns={'name':'column_name'}, inplace=True)
    value_compare_df["time"] = temp_time
    value_compare_df["stk_id"] = col
    value_compare_df["type"] = "data"
    if 'std' in value_compare_df.columns:
        execute_values(conn, value_compare_df, 'plc_abnormal_log')
    else: 
        pass

    ###result_col_insert
    col_compare_df = pd.concat([df1,df2,df3,df9,temp_df],axis = 1)
    col_compare_df["time"] = temp_time
    col_compare_df["stk_id"] = col
    col_compare_df["type"] = "column" 
    col_compare_df["column_name"] = "null"
    if 'std' in col_compare_df.columns:
        execute_values(conn, col_compare_df, 'plc_abnormal_log')
    else:
        pass

    #check stk insert
    inserttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    check_nowtime = {'time':inserttime}
    time_df = pd.DataFrame([check_nowtime])
    auto_df_to_db(time_df,df2,"check","null","null","null") 

   







