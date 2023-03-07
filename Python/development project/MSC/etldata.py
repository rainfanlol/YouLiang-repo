#!/usr/bin/python3
#coding:utf-8

import csv
import os
import pandas as pd
import time
import glob


def main():
    path = '/home/mirle/workspace/msc/etl/'
    allFileList = os.listdir(path)
    ip=allFileList[0]
    dirpath=r"/home/mirle/workspace/msc/etl/*/*.csv"    
    filepath=glob.glob(dirpath)
    str = filepath[0]
    filename=str.split('/')
    df = pd.read_csv(filepath[0],encoding= 'Big5')
    inserttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    df['insert_date_time'] = inserttime    
    df['msc_ip'] = ip
    df['file_name'] = filename[-1]    
    df.to_csv(filepath[0], index=False)
    destination="/home/mirle/workspace/msc/public/"+filename[-1]
    publicpath='/home/mirle/workspace/msc/public'
    if not os.path.isdir(publicpath):
     os.makedir('public')
    os.rename(filepath[0],destination)

main()
