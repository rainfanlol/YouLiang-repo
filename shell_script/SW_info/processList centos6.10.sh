#!/bin/bash
#pslist=`ps -eo user,pid,ppid,%cpu,%mem,stime,time,cmd --sort=-user`
#pslist=`ps -eo user,%cpu,%mem,pid,cmd --sort=-user`
#echo "${pslist}"
pslist=`ps -eo user,%cpu,%mem,pid,cmd --sort=-%cpu,-rss,-user | head -n 1500`

##包含ken
echo "${pslist}"
