#!/bin/bash
#pslist=`ps -eo user,pid,ppid,%cpu,%mem,stime,time,cmd --sort=-user`
#pslist=`ps -eo user,%cpu,%mem,pid,cmd --sort=-user`
#echo "${pslist}"
pslist=`ps -eo user,%cpu,%mem,pid,cmd | awk 'NR<2{print $0;next}{print $0| "sort -k2nr -k3nr |head -n 1500"}'`

##包含ken
echo "${pslist}"
