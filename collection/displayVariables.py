from sys import modules
# 在idle中import该模块,可以用 who 或 whos() 显示变量
# 1,是展示 __repr__ 的用处
# 2,是可以使用 sys 里的 modules 看到其他frame里的变量
def asterisk():
    a = 30*'***'
    print(a)

# for k in filter(lambda a: (not a.startswith('_')) & (len(a) < 8),dir()) : print(k)
class DISPVARS:
    def __repr__(self):
        a = (k for k in dir( modules['__main__'] ) if  k[0]!='_' and len(k)<=10 )
        b=sorted(a, key=len)
        for c in b : print(c,end='\t')
        print()
        return 30*'***'

who=DISPVARS()

def whos(N=20):
##    for a in (k for k in dir() if k[0]!='_' ) : print(a,end='\t')
    asterisk()
    a = (k for k in dir( modules['__main__'] ) if  k[0]!='_' and len(k)<=N )
    b=sorted(a, key=len)
    for c in b : print(c,end='\t')
    print()
    asterisk()



