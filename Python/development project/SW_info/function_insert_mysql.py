#!/usr/bin/python3

#########################################
#                                       #
# edit by criz 2020/02/12 version 1.1   #
#                                       #
#########################################

import sys, os, time
from function_you.function_ospopen import *

########## function_insert_mysql
def function_insert_mysql(sqldict,tablename,database):      
#sqldict = {'icin_host_object_id':objectid, 'Device':displayname, 'APIname':apiname, 'dataKey':key, 'dataValue':value, 'status':status, 'layer':layer, 'insert_date':dateTime}

	########## found key with value
	allkeys = []
	truekeys = []
	allkeys = sqldict.keys()
	for count in range(len(sqldict)):
		if ( sqldict[allkeys[count]] != "" ):
                        truekeys.append(allkeys[count])

	########## sqlkey && sqlvalue
	sqlkey = ""
	sqlvalue = ""
	for count in range(len(truekeys)):
		if ( sqlkey == "" ):
			sqlkey = truekeys[count]
			sqlvalue = "'"+sqldict[truekeys[count]]+"'"
		else:
			sqlkey = sqlkey+", "+truekeys[count]
			sqlvalue = sqlvalue+", "+"'"+sqldict[truekeys[count]]+"'"

	########## sqlstr
	sqlstr = "INSERT INTO "+tablename+" ("+sqlkey+") VALUES ("+sqlvalue+");"

	########## insert into sql
	function_ospopen("sudo mysql -D %s -e \"%s\"" % (database,sqlstr))

########## function_query_mysql
def function_query_mysql(command,database):
	
	########## query mysql
	revalue = function_ospopen("sudo mysql -D %s -e \"%s\"" % (database,command))
	
	########## return value
	return revalue

