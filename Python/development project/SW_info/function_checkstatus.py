#!/usr/bin/python3
#目標:判斷title的status
#參數可給List只要出現2就跳出迴圈判斷為2,出現1還是會把List都檢查完,結果判斷都沒問題則會判為0


###參數給List判斷titlestatus值
def TitleStatus(Lis):
 ReSult = 0
 Lis=[int(i) for i in Lis]
 for i in range(len(Lis)):
  if (Lis[i] == 3 and ReSult !=1):
     ReSult = 3
     continue
  elif (Lis[i] == 1 ):
     ReSult = 1
     continue
  elif (Lis[i] == 2 ):
     ReSult = 2
     return ReSult
     break
  else:
     continue
 return ReSult
