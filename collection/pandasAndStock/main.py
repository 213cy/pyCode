import pandas as pd
import numpy as py
from datetime import datetime
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

df.info()
dl.info()

print( pd.DataFrame(zip(dl.open,df.open),columns=['a','b']) )

logindex= dl['high'] == df['high']
a = pd.DataFrame( (dl['high'][~logindex],df['high'][~logindex]),('fromfile','fromweb'))
print(a)

a= dl.low == df.low
a.any(),a.all()
(dl.low.isin( df.low) == a).all()
print( pd.DataFrame.equals(dl.low,df.low) ) # False

b=dl.close.diff().round(2)
b[0] =  dl.loc[0,'change']
print( pd.DataFrame.equals(b,dl.change) )

c=100 * b[1:] /dl.close[0:-1].values
c[0]=dl.loc[0,'change_percent']
c.sort_index(inplace=True)
print( dl.change_percent.equals(c.round(2)) )

d= 100*(dl.high[1:]-dl.low[1:] )/dl.close[:-1].values
print( d.round(2).equals(dl.振幅[1:]) )
