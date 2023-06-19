import os,sys
import psutil

print('===================')
print(sys.prefix)
print(sys.executable)
filename = sys.argv[0].lower()
print(filename,'   pid =',os.getpid())

ppid =os.getppid()
pp = psutil.Process(ppid)
print( pp.cmdline() )
print( pp.name() ,'   ppid =',ppid)

print('-------------------')

pd = {}
for prcs in psutil.process_iter():
    a = list( map(str.lower, prcs.cmdline()) )
    # print(prcs.pid ,a)
    if filename in a:
        pd[prcs.pid] = a.index(filename)
        print(prcs.pid,'---',os.getppid(),a)

raise BaseException
print('afd')
