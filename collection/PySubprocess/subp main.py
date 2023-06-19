import subprocess as sp

b=sp.PIPE
print(type(b),'\n')


a=sp.Popen(['python','subp test.py'],stdout=b,stderr=b)
print('------ Popen with shell = False (default)     subprocess.pid =', a.pid)
c=a.stdout.read()
print(c.decode())
print('---------')
c=a.stderr.read()
print(c.decode(encoding='gb2312'))


a=sp.Popen('subp test.py',shell=True,stdout=b,stderr=b)
print('------ Popen with shell = True     subprocess.pid =', a.pid)
c=a.stdout.read()
print(c.decode())
print('---------')
c=a.stderr.read()
print(c.decode(encoding='gb2312'))
