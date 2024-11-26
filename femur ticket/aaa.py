import pandas as pd
import numpy as py
from datetime import datetime
import matplotlib.pyplot as plt
from xxx import *


fileA='aaa.csv'
df = pd.read_csv(fileA,sep='\t',header=1,encoding='gb2312')

temp=df.columns
t=[datetime.strptime(k,'%m/%d/%Y') for k in df[temp[0]]]
print( b'\xc8\xd5\xc6\xda'.decode('gb2312').encode('gb2312') )

df.columns=['date', 'open', 'high', 'low', 'close' ,'volume','total']
df.date=pd.to_datetime (df.date)
start_date=df.date[0].strftime('%Y%m%d')
end_date=df.date.iloc[-1].strftime('%Y%m%d')
##############
# dl=stock_zh_a_hist("000001", "daily", '20070111', '20120629', "")
dl=stock_zh_a_hist("000001", "daily", start_date, end_date, "")

##############


#raise SystemExit



'''HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'''

plt.style.available
 
fig, ((ax1,ax2), (ax3,ax4)) = plt.subplots(2,2,figsize=(10,10))
fig.autofmt_xdate(rotation = 45)

ax1.plot(t, features['open'])
ax1.set_xlabel(''); ax1.set_ylabel('yuan'); ax1.set_title('open')


ax2.plot(t, features['high'])
ax2.set_xlabel(''); ax2.set_ylabel('yuan'); ax2.set_title('high')

plt.style.use('fivethirtyeight')

ax3.plot(t, features['low'])
ax3.set_xlabel(''); ax3.set_ylabel('yuan'); ax3.set_title('low')

ax4.plot(t, features['close'])
ax4.set_xlabel(''); ax4.set_ylabel('yuan'); ax4.set_title('close')

plt.show()
print('asdfsdf')

'''HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'''
