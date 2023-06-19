set prefix=D:\Anaconda3
set addpath=%prefix%;%prefix%\Library\mingw-w64\bin
set addpath=%addpath%;%prefix%\Library\usr\bin
set addpath=%addpath%;%prefix%\Library\bin
set addpath=%addpath%;%prefix%\Scripts\
REM set path=%addpath%;%path%
set path=%addpath%

set PYTHONSTARTUP=C:\Users\Administrator\Documents\python\runscript\idle\startup.py

start /D C:\Users\Administrator\Documents\python ^
D:\Anaconda3\pythonw.exe ^
D:\Anaconda3\Lib\idlelib\idle.pyw -s

REM start /D C:\Users\Administrator\Documents\python ^
REM D:\Anaconda3\pythonw.exe ^
REM D:\Anaconda3\Lib\idlelib\idle.pyw -c "from torch import *"