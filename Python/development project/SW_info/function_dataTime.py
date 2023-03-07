#!/usr/bin/python3

#########################################
#                                       #
# edit by Ransom                        #
# 2020/02/24 created                    #
#                                       #
#########################################

import time

def function_getDataTime():
	localDateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	return localDateTime
