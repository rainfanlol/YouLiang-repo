#!/usr/bin/python3

#########################################
#                                       #
# edit by Criz                          #
# 2020/02/06 created                    #
#                                       #
#########################################

import sys, os

########## function_query_oracle
def function_ospopen(command):
	
	########## 
	osp = os.popen("%s" % command)
	popvalue = osp.read()
	osp.close()
	
	########## return
	return popvalue

