import sys

# from notebook.notebookapp import main
from spyder.app.start import main

if __name__ == '__main__':
    sys.argv[0] = sys.argv[1]
    sys.exit(main())
