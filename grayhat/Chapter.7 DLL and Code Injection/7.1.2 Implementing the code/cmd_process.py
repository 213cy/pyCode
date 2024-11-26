import subprocess
import time


# when Popen is called with shell=True,
# wShowWindow is fixed to SW_HIDE
subpp = subprocess.Popen(
    'cmd \k', creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.PIPE,
    stdin=subprocess.PIPE)
print(f"PID: {subpp.pid}     poll stat: {subpp.poll()}")

exit()

# when Popen is called with shell=True,
# wShowWindow is fixed to SW_HIDE
subpp = subprocess.Popen(
    'cmd', shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
print(f"PID: {subpp.pid}     poll stat: {subpp.poll()}")

exit()


subpp = subprocess.Popen('cmd /k echo asdfsdf',
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
print(f"PID: {subpp.pid}     poll stat: {subpp.poll()}")
# subpp=subprocess.Popen('cmd',shell=True)

exit()

si = subprocess.STARTUPINFO()
si.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
si.dwFlags = subprocess.STARTF_USESHOWWINDOW
SW_SHOW = 5
SW_HIDE = 0
SW_MAXIMIZE = 3
si.wShowWindow = SW_HIDE
si.wShowWindow = SW_MAXIMIZE
# when Popen is called with shell=True,
# wShowWindow is fixed to SW_HIDE
subpp = subprocess.Popen(
    'cmd', creationflags=subprocess.CREATE_NEW_CONSOLE, startupinfo=si)
print(f"PID: {subpp.pid}     poll stat: {subpp.poll()}")

exit()


# =================================
# taskkill /im cmd.exe
# tasklist /fi "imagename eq cmd.exe" /nh
# tasklist /fi "imagename eq cmd.exe" /nh | find /c "cmd"
# =================================


exit()
args = 'cmd /k echo victim process has been killed by me!!'
subpp = subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(f"PID: {subpp.pid}     poll stat: {subpp.poll()}")

# print(subpp.stderr.read1())
print(subpp.stdin.write(b'dir\n'))
print(subpp.stdin.flush())
print(subpp.stdout.read1())
# print(subpp.stdout.read1())
# print(subpp.stdout.read1())
# print(subpp.stdout.read1())
# print(subpp.stdout.read1())

print(subpp.poll())
exit()
