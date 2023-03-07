#!/usr/bin/python3
#coding:utf-8

import os
import sys
from os import walk
from os.path import join
import shutil

def main():
 rawdatapath = '/home/mirle/workspace/msc/curve/nas' 
 stagpath= '/home/mirle/workspace/msc/etl/'


 for root, dirs, files in walk(rawdatapath):
  for f in files:
    fullpath = join(root, f)
    ipname = root.split('/')
    destination = join(stagpath,ipname[-1])
    fdestination = destination+"/"+f
    command='find ' +stagpath+ ' -type d -empty -delete'
    os.popen(command)
    #if not os.path.isdir(stagpath):
     #os.makedir('etl')
    if not os.path.isdir(destination):
     os.makedirs(destination)
    shutil.move(fullpath,destination)
    #print(fullpath)
    #print(ipname)
    #print(destination)
    sys.exit()
main()
