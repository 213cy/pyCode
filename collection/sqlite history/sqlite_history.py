import sqlite3
import pandas as pd


path='C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
##path='E:\\Program Files\\DB Browser for SQLite\\History'

con = sqlite3.connect(path)

cur = con.cursor()
temp=cur.execute('SELECT url FROM visits')
a=pd.DataFrame (temp)
temp=cur.execute('SELECT id,url FROM urls')
b=pd.DataFrame (temp,columns=['ind','url'])


dfa = pd.read_sql_query('SELECT url FROM visits', con)
dft = pd.read_sql_query('SELECT visit_time FROM visits', con)
dfb = pd.read_sql_query('SELECT id,url FROM urls', con)

con.close()

##############

Nvisit = dfa.size
Nurl = dfa.url.unique().size
print(f'数据库中记录了 {Nvisit} 条访问信息,其中共访问了 {Nurl} 个网点')

aa=dfa.value_counts().reset_index()
aa.columns=['id','num']
##dfb.sort_values(by='id')
print(aa.count().id, dfa.value_counts().size, aa.shape[0], len(aa) )
print(aa.size)

##############
# 11644502400.0	11644473600.0
'''
下面这一行是个sql语句 不是pyhon的
datetime("visit_time" / 1000000 - 11644473600 + 28800, 'unixepoch')
'''
tt =dft.apply ([min,max]) - 11644473600.0 * 1000000 + 28800 * 1000000
tt= tt.apply(pd.to_datetime ,axis=0,unit='us')
t1 = str(tt.visit_time[0])[:19]
t2 = (tt.at['max','visit_time'].__str__())[:19]
print( f'时间区间为: {t1} ~ {t2}' )
##############
def gethostname(k):
	s= k[ k.find('//')+2 : k.find('/',10) ] 
	m=len(s)
	n = s.rfind('.')
##	breakpoint()
	while n>m-5 and n>-1:
		s= s[0:n]
		m=n
		n = s.rfind('.')
##	if len(s) <4 : print(k)
	if n>-1:
		s = s[n+1:]
	return s

def gethost(k):
	s= k[ k.find('//')+2 : k.find('/',10) ] 
	a = s.split('.')
	n = len(a)
	if n >= 4:
		if a.count('qq'):  return 'qq'
		for k in a[::-1]:
			if len(k)>3 : return k
		return a[1]
	elif n == 3:
		return a[1]
	else:
		return a[0]


##dfb.url=dfb.url.apply( lambda x : x[x.find('//')+2:x.find('/',10)] )
dfb.url=dfb.url.apply( gethost )

bb=pd.merge(aa,dfb,how='inner',on='id')
cc=bb[['num','url']].groupby('url').sum()
dd= cc.sort_values('num',ascending=False)
print(30*'==')
print(dd[0:30])
##breakpoint()


