# this script is used on windows to wrap shortcuts so that they are executed within an environment
#   It only sets the appropriate prefix PATH entries - it does not actually activate environments

import os
import sys
import subprocess
from os.path import join, pathsep

# call as: python cwp.py PREFIX ARGs...

prefix = 'D:\\Anaconda3'
new_paths = pathsep.join([prefix,
                         join(prefix, "Library", "mingw-w64", "bin"),
                         join(prefix, "Library", "usr", "bin"),
                         join(prefix, "Library", "bin"),
                         join(prefix, "Scripts")])
env = os.environ.copy()
# env['PATH'] = new_paths + pathsep + env['PATH']
env['PATH'] = new_paths
env['CONDA_PREFIX'] = prefix
# env['PYTHONSTARTUP']  = r'C:\Users\Administrator\Documents\python\runscript\idle\startup.py'
env['PYTHONSTARTUP']  = 'C:\\Users\\Administrator\\Documents\\python\\runscript\\idle\\startup.py'

documents_folder = 'C:\\Users\\Administrator\\Documents\\python'
os.chdir(documents_folder)

args = ['D:\\Anaconda3\\pythonw.exe'
, r'C:\Users\Administrator\Documents\python\runscript\idle\script.py'
# ,'-m torch'
# ,'-i'
]

sys.exit(subprocess.call(args, env=env))
