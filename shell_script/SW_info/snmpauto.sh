#!/bin/sh
# Program:
#       自動登入遠端多台電腦並安裝snmp服務和開啟防火牆port161&162
# History:
# 2020/02/25    VBird   First release
# 2020/02/27    新增防火牆設定
# 2020/03/04    讀取ip方式更改
# 2020/03/05    新增系統判斷和防火牆是否開啟
# 2020/03/06    修改RPM安裝和原始OS有無SNMP套件確認
# 2020/03/11    更新ISO-SNMP安裝方法


for i in `cat hosts.txt`
do

echo "目前執行ip:"$i

scp -r /root/LinSNMPservice/oscheck.sh $i:/root/



ssh -tt $i "sh /root/oscheck.sh;rm -rf /root/LinSNMPservice /root/oscheck.sh;exit"
done

