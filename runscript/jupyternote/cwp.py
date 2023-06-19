# this script is used on windows to wrap shortcuts so that they are executed within an environment
#   It only sets the appropriate prefix PATH entries - it does not actually activate environments

import os
import sys
import subprocess
from os.path import join, pathsep

# call as: python cwp.py PREFIX ARGs...

# prefix = sys.argv[1]
prefix = 'D:\\Anaconda3'
documents_folder = 'C:\\Users\\Administrator\\Documents\\python\\jupyternote\\'
# args = sys.argv[2:]
args = ['D:\\Anaconda3\\python.exe', 
sys.argv[0][:-6] + 'script.py', 
'C:\\Users\\Administrator\\Documents\\python\\jupyternote\\']

new_paths = pathsep.join([prefix,
                         join(prefix, "Library", "mingw-w64", "bin"),
                         join(prefix, "Library", "usr", "bin"),
                         join(prefix, "Library", "bin"),
                         join(prefix, "Scripts")])
env = os.environ.copy()
env['PATH'] = new_paths + pathsep + env['PATH']
env['CONDA_PREFIX'] = prefix


os.chdir(documents_folder)

sys.exit(subprocess.call(args, env=env))
