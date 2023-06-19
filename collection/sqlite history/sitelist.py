import sqlite3
import pandas as pd


path='C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
con = sqlite3.connect(path)

df = pd.read_sql_query('SELECT last_visit_time,url FROM urls', con)

con.close()


##############
# 11644502400.0	11644473600.0
'''
下面这一行是个sql语句 不是pyhon的
datetime("visit_time" / 1000000 - 11644473600 + 28800, 'unixepoch')

##tt =dft.apply ([min,max]) - 11644473600.0 * 1000000 + 28800 * 1000000
##tt= tt.apply(pd.to_datetime ,axis=0,unit='us')
##t1 = str(tt.visit_time[0])[:19]
'''


def gethost(k):
        ind = k.rfind('//')
        a = k[ind+2:].split('/')[0]
        return a

df.url=df.url.apply( gethost )
aa=df.groupby('url').max()
bb= aa[aa.last_visit_time>1000]
bb=bb.copy()
##https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
bb.loc[:,'last_visit_time'] = pd.to_datetime(
        bb.last_visit_time - 11644473600.0 * 1000000 + 28800 * 1000000,
        unit='us')
bb.last_visit_time=bb.last_visit_time.apply(pd.Timestamp.strftime ,args=('%Y-%m-%d',))
bb.sort_values('last_visit_time',ascending=False,inplace=True)

cc=bb.copy()
cc.reset_index(inplace=True)
cc.set_index('last_visit_time',inplace=True)

K=0
while input('type any key to break ==>') == '':
        dd = cc[K:K+20]
        print( dd )
        K = K+20

##breakpoint()


