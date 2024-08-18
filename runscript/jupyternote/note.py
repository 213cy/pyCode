# this script is used on windows to wrap shortcuts so that they are executed within an environment
#   It only sets the appropriate prefix PATH entries - it does not actually activate environments

import os
import sys
import subprocess
from os.path import join, pathsep

# call as: python cwp.py PREFIX ARGs...


documents_folder = 'E:\\Documents\\pyCode\\jupyternote'
print( os.getcwd() == documents_folder )
os.chdir(documents_folder)

# breakpoint()

###############################
# prefix = sys.argv[1]
##prefix = 'D:\\Python38'
##
##new_paths = pathsep.join([prefix,
##                         join(prefix, "Library", "mingw-w64", "bin"),
##                         join(prefix, "Library", "usr", "bin"),
##                         join(prefix, "Library", "bin"),
##                         join(prefix, "Scripts")])
env = os.environ.copy()
##env['PATH'] = new_paths + pathsep + env['PATH']
###############################


# args = sys.argv[2:]
args = ['D:\\python38\\python.exe', 
sys.argv[0][:-7] + 'script.py', 
'E:\\Documents\\pyCode\\jupyternote']




breakpoint()
sys.exit(subprocess.call(args, env=env))
