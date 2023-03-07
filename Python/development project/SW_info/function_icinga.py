#!/usr/bin/python3

#########################################
#                                       #
# edit by criz 2020/02/12 version 1.1   #
#                                       #
#########################################

import sys, os, time
from function_you.function_insert_mysql import function_query_mysql

########## function_icinga_displayname
def function_icinga_displayname(hostip):

	########## default variable
	command = "SELECT icinga_hosts.display_name FROM icinga2.icinga_hosts LEFT JOIN icinga2.icinga_objects ON icinga_hosts.host_object_id = icinga_objects.object_id WHERE icinga_hosts.address = '"+hostip+"' AND icinga_objects.is_active = 1;"
	database = "icinga2"

	########## get dissplayname
	revalue = function_query_mysql(command,database).splitlines()[1]
	
	########## return
	return revalue

##########
def function_icinga_objectid(hostip,displayname):

	########## default variable
	command = "SELECT icinga_hosts.host_object_id FROM icinga2.icinga_hosts LEFT JOIN icinga2.icinga_objects ON icinga_hosts.host_object_id = icinga_objects.object_id WHERE icinga_hosts.address = '"+hostip+"' AND icinga_objects.is_active = 1 AND icinga_hosts.display_name = '"+displayname+"';"
	database = "icinga2"

	########## get objectid
	revalue = function_query_mysql(command,database).splitlines()[1]

	########## return
	return revalue
